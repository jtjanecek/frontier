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

class View():
	def __init__(self):
		self._boundary = None
		self._state = 'initialized'
		self._data_lock = threading.Lock()

	def get_state(self):
		result = None
		with self._data_lock:
			result = deepcopy(self._state)
		return result

	def calibrate(self):
		max_tries = 20

		print("Calibrating view... Try #1...")
		image = self._screenshot()
		image = image.convert('LA')
		results = self._ocr(image)

		tries = 1
		while 'continue' not in results.keys():
			if tries == max_tries:
				print("Could not find a valid 'CONTINUE'!")
				sys.exit()
			tries += 1
			print("Calibrating view... Try #{}...".format(tries))
			image = self._screenshot()
			image = image.convert('LA')
			results = self._ocr(image)
		continueBox = results['continue']['loc']
		
		continueXLen = abs(continueBox[0][0]-continueBox[1][0])
		continueYLen = abs(continueBox[0][1]-continueBox[1][1])
	
		leftBoundary = continueBox[0][0] - (continueXLen*0.3178807947)
		topBoundary = continueBox[0][1] - (continueYLen*1.2)
		rightBoundary = leftBoundary + (continueXLen*5.05)
		bottomBoundary = topBoundary + (continueYLen*17)
		
		self._boundary=((leftBoundary, topBoundary, rightBoundary, bottomBoundary))

		#image = self._screenshot()
		#results = self._ocr(image)
		#image.show()

		self._state = 'continue'

	def start(self):
		self._thread = threading.Thread(target=self._main_loop, daemon=True)
		self._thread.start()

	def _main_loop(self):
		while True:
			image = self._screenshot()
			#image.show()
			#sys.exit()
			results = self._ocr(image)

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
		return image

	def _ocr(self,image):
		conf = '--oem 1'
		results = pytesseract.image_to_data(image, output_type=Output.DICT, config=conf)
		#results = pytesseract.image_to_string(image)
		print('OCR results:',' '.join([text for text in results['text'] if text != '']))
	
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

	import time; time.sleep(100)
