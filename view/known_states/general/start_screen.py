from utils.utils import text_similarity

class StartScreen():
	def __init__(self, config):
		self._config = config
		self._state = {'location': 'general', 'context': 'start screen'}

		self._text_conditions = [
			"CONTINUE",
		]
	
	def check(self, ocr_text):
		for text in self._text_conditions:
			if text_similarity(text, ocr_text) >= self._config['text_sim_threshold']:
				return True
		return False

	def get_state(self):
		return self._state
