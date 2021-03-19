from view.view import View
import logging
#logging.basicConfig(level=logging.DEBUG,
#	format='%(asctime)s - %(module)s - %(levelname)s - %(message)s',
#	datefmt='%m-%d-%y %H:%M')
logger = logging.getLogger('frontier')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

v = View()
v.calibrate()
v.start()

import time
while True:
	time.sleep(1)
