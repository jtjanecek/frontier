from utils.utils import text_similarity

class LevelChoice():
	def __init__(self, config):
		self._config = config
		self._state = {'location': 'factory', 'context': 'level 50 or open level'}

		self._text_conditions = [
			"which level do you wish to challenge level 50 or open level",
		]
	
	def check(self, ocr_text):
		for text in self._text_conditions:
			if text_similarity(text, ocr_text) >= self._config['text_sim_threshold']:
				self._state['text'] = text
				return True
		return False

	def get_state(self):
		return self._state
