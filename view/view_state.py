from PIL import Image


class ViewState():
	def __init__(self):
		self._state = {'state': 'continue screen', 'text': 'continue', 'context': 'start screen'}


	def process(self, image: Image, ocr_results: dict):
		return True

	def calibrate(self):
		pass

	def __str__(self) -> str:
		return str(self._state)





