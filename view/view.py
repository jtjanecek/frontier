import os.path
import time
import sys
from collections import defaultdict
from PIL import Image, ImageDraw
import numpy as np
import pyautogui
import cv2
import pytesseract
from pytesseract import Output
from copy import deepcopy
import threading
from .view_state_manager import ViewStateManager
import logging
import json
logger = logging.getLogger('frontier.view')

class View():
	def __init__(self):
		self._boundary = None
		self._state_manager = ViewStateManager()
		self._data_lock = threading.Lock()
		self._screenshot_counter = 0

		self._dir_path = os.path.dirname(os.path.realpath(__file__))
		boundary_file = os.path.join(self._dir_path,'boundary.json')
		if os.path.isfile(boundary_file):
			with open(boundary_file) as f:
				jsondata = json.loads(f.read())
				self._boundary = ((jsondata['leftBoundary'], jsondata['topBoundary'], jsondata['rightBoundary'], jsondata['bottomBoundary']))
				logger.info(f"Boundary configuration found! Using boundary configuration: {jsondata}")
		
	def get_state(self):
		state = None
		with self._data_lock:
			state = deepcopy(self._state_manager.get_state())
		return state

	def calibrate(self):
		max_tries = 20
		
		if self._boundary != None:
			logger.info("View calibrated!")
			return

		#logger.info("Calibrating view... Try #1...")
		image = self._screenshot()
		image = image.convert('LA')
		results = self._ocr(image)
	
		logger.info("Position your mouse at the TOP LEFT of the emulator screen...")
		for i in range(10,0,-1):
			logger.info(f"Capturing in {i} second(s)...")
			time.sleep(1)
		topleft = pyautogui.position()
		topBoundary = topleft.y
		leftBoundary = topleft.x
		logger.info(topleft)

		logger.info("Position your mouse at the BOTTOM RIGHT of the emulator screen...")
		for i in range(10,0,-1):
			logger.info(f"Capturing in {i} second(s)...")
			time.sleep(1)
		bottomright = pyautogui.position()
		rightBoundary = bottomright.x
		bottomBoundary = bottomright.y
		logger.info(bottomright)

		self._boundary=((leftBoundary, topBoundary, rightBoundary, bottomBoundary))
		boundary_json = {'leftBoundary': leftBoundary, 'topBoundary': topBoundary, 'rightBoundary': rightBoundary, 'bottomBoundary': bottomBoundary}
		boundary_path = os.path.join(self._dir_path,'boundary.json')
		with open(boundary_path, 'w') as outfile:
			json.dump(boundary_json, outfile)
		logger.info(f"Saved boundary to: {boundary_path}")
		logger.info("View calibrated!")

	def start(self):
		self._thread = threading.Thread(target=self._main_loop, daemon=True)
		self._thread.start()

	def _main_loop(self):
		while True:
			image = self._screenshot()
			results = self._ocr(image)
			with self._data_lock:
				changed = self._state_manager.update_state(image, results)
				if changed == True:
					logger.info("New state: " + str(self._state_manager.get_state()))	

	def _screenshot(self):
		image = pyautogui.screenshot()

		if self._boundary == None:
			width,height = image.size
			left = 0
			right = width * .4
			top = 0
			bottom = height/2
			self._boundary = ((left,top,right,bottom))
		image = image.crop(self._boundary)
		self._screenshot_counter += 1
		if self._screenshot_counter % 50 == 0:
			image.save("view/.screenshot.png","PNG")
		return image

	def _ocr(self,image):
		conf = '--oem 1'
		results = pytesseract.image_to_data(image, output_type=Output.DICT, config=conf)
		logger.debug('OCR results: ' + ' '.join(results['text']))
	
		results_dict = defaultdict(dict)
		for i in range(0, len(results["text"])):
			# extract the bounding box coordinates of the text region from
			# the current result
			text = results['text'][i].strip().lower()
			if text == '':
				continue
			x = results["left"][i]
			y = results["top"][i]
			w = results["width"][i]
			h = results["height"][i]
			# extract the OCR text itself along with the confidence of the
			# text localization
			conf = int(results["conf"][i])
			results_dict[text]['loc'] = ((x,y),(x+w,y+h))
		return results_dict

	def _draw_rectangle(self, image, coordinates, color='black', width=5):
		draw = ImageDraw.Draw(image)
	
		for i in range(width):
			rect_start = (coordinates[0][0] - i, coordinates[0][1] - i)
			rect_end = (coordinates[1][0] + i, coordinates[1][1] + i)
			draw.rectangle((rect_start, rect_end), outline = color)

		import matplotlib.pyplot as plt
		plt.imshow(image)
		plt.show()


if __name__ == '__main__':
	v = View()
	v.calibrate()
	v.start()
		
	import time
	while True:
		time.sleep(1)

