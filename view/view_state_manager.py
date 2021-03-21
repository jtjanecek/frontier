import os
import types
from PIL import Image
from utils.utils import text_similarity
import logging
import glob
logger = logging.getLogger("frontier.viewstatemanager")

class ViewStateManager():
	def __init__(self):
		self._state = {'location': 'start screen'}
		self._state_config = {'text_sim_threshold': .8}
		self._known_states = self._initialize_states()

	def get_state(self):
		return self._state

	def update_state(self, image: Image, ocr_results: str):
		'''Update the state of the view from the ocr results and image

		Return:
			boolean: if the state has been changed
		'''
		ocr_text = ' '.join(ocr_results.keys())

		passing_states = []
		for state in self._known_states:
			if state.check(ocr_text):
				passing_states.append(state)
		
		if len(passing_states) >= 2:
			logger.error(f">2 states found for text: {ocr_text}")
			logger.error(str(passing_states))
			raise Exception()

		if len(passing_states) == 0:
			return False
	
		new_state = passing_states[0].get_state()
		if new_state == self._state:
			return False
		self._state = new_state
		return True

	def __str__(self) -> str:
		return str(self._state)


	def _initialize_states(self) -> list:
		states = []

		dir_path = os.path.dirname(os.path.realpath(__file__))
		
		factory_path = os.path.join(dir_path, 'known_states', 'factory')

		modules = glob.glob(os.path.join(factory_path, '*.py'))

		for module in modules:
			module = os.path.basename(module).split(".")[0]
			module_camel = ''.join([temp.capitalize() for temp in module.split("_")])
			import_statement = f"from .known_states.factory.{module} import {module_camel} as Factory{module_camel}"
			logger.debug(f"State import: {import_statement}")
			exec(import_statement)
			exec(f"states.append(Factory{module_camel}({self._state_config}))")
		return states

