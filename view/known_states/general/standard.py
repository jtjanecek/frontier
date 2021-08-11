from utils.utils import text_similarity

class Standard():
	def __init__(self, config):
		self._config = config
		self._state = {'location': 'general', 'context': 'intro text'}

		self._text_conditions = [
			"where the intelligence of trainers is put to the test",
			"welcome to the battle factory",
			"i am your guide to the battle swap single tournament",
			"would you like to take the battle swap single challenge",
			"before you begin your challenge i need to save the game is that okay",
			"battle frontier player badges would you like to save the game",
			"battle frontier player badges there is already a saved file is it okay to overwrite it",
			"please step this way"
		]
	
	def check(self, ocr_text):
		for text in self._text_conditions:
			if text_similarity(text, ocr_text) >= self._config['text_sim_threshold']:
				self._state['text'] = text
				return True
		return False

	def get_state(self):
		return self._state
