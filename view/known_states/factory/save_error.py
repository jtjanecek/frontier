from utils.utils import text_similarity

class SaveError():
	def __init__(self, config):
		self._config = config
		self._state = {'location': 'factory', 'context': 'reset game without saving text'}

		self._text_conditions = [
			"im sorry to say this but you didnt save before you quit playing last time",
			"as a result you have been disqualified from your challenge",
		]
	
	def check(self, ocr_text):
		for text in self._text_conditions:
			if text_similarity(text, ocr_text) >= self._config['text_sim_threshold']:
				return True
		return False

	def get_state(self):
		return self._state
