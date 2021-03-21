from view.view import View
import logging
import os
#logging.basicConfig(level=logging.DEBUG,
#	format='%(asctime)s - %(module)s - %(levelname)s - %(message)s',
#	datefmt='%m-%d-%y %H:%M')
logger = logging.getLogger('frontier')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
logger.addHandler(sh)
filehandler = logging.FileHandler(os.path.join('logs','frontier.log'), mode='w')
filehandler.setFormatter(formatter)
filehandler.setLevel(logging.DEBUG)
logger.addHandler(filehandler)

v = View()
v.calibrate()
v.start()

import time
while True:
	time.sleep(1)
