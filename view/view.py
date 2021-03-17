import sys
from collections import defaultdict
from PIL import Image, ImageDraw
import numpy as np
import pyautogui
import cv2
import pytesseract
from pytesseract import Output
from copy import deepcopy



class View():
	def __init__(self):
		self._boundary = None
		self._state = 'initialized'

	def get_state(self):
		return deepcopy(self._state)

	def calibrate(self):
		max_tries = 20

		print("Calibrating view... Try #1...")
		image = self.screenshot()
		image = image.convert('LA')
		results = self.ocr(image)

		tries = 1
		while 'continue' not in results.keys():
			if tries == max_tries:
				print("Could not find a valid 'CONTINUE'!")
				sys.exit()
			tries += 1
			print("Calibrating view... Try #{}...".format(tries))
			image = self.screenshot()
			image = image.convert('LA')
			results = self.ocr(image)
		continueBox = results['continue']['loc']
		
		continueXLen = abs(continueBox[0][0]-continueBox[1][0])
		continueYLen = abs(continueBox[0][1]-continueBox[1][1])
	
		leftBoundary = continueBox[0][0] - (continueXLen*0.3178807947)
		topBoundary = continueBox[0][1] - (continueYLen*1.2)
		rightBoundary = leftBoundary + (continueXLen*5.12)
		bottomBoundary = topBoundary + (continueYLen*18.5)
		
		self._boundary=((leftBoundary, topBoundary, rightBoundary, bottomBoundary))

		'''
		image = self.screenshot()
		image.show()
		results = self.ocr(image)
		image = image.convert('LA')
		results = self.ocr(image)
		image.show()
		'''

		self._state = 'continue'

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
		print('OCR results:',[text for text in results['text'] if text])
	
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


v = View()
print(v.get_state())
v.calibrate()
print(v.get_state())
