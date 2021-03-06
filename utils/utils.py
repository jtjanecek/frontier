import os
import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import logging
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
filehandler = logging.FileHandler(os.path.join('logs','utils.log'), mode='w')
filehandler.setFormatter(formatter)
filehandler.setLevel(logging.DEBUG)
logger.addHandler(filehandler)

def text_similarity(expected_input: str, got_input: str):
	expected = re.sub(r'[^\w\s]', '', expected_input.lower()) 
	got = re.sub(r'[^\w\s]', '', got_input.lower()) 

	expected = ' '.join(expected.split())
	got = ' '.join(got.split())

	word_list = expected.split()

	X = expected
	Y = got

	X_list = word_tokenize(X)  
	Y_list = word_tokenize(Y) 

	# sw contains the list of stopwords 
	sw = stopwords.words('english')  
	l1 =[];l2 =[] 
  
	# remove stop words from the string 
	X_set = {w for w in X_list if not w in sw}  
	Y_set = {w for w in Y_list if not w in sw} 
  
	# form a set containing keywords of both strings  
	rvector = X_set.union(Y_set)  
	for w in rvector: 
		if w in X_set: l1.append(1) # create a vector 
		else: l1.append(0) 
		if w in Y_set: l2.append(1) 
		else: l2.append(0) 
	c = 0
  
	# cosine formula  
	for i in range(len(rvector)): 
		c+= l1[i]*l2[i] 
	if sum(l1) == 0 or sum(l2) == 0:
		cosine = 0
	else:
		cosine = c / float((sum(l1)*sum(l2))**0.5) 
	logger.debug(f"text_sim: expected:[{expected}] got:[{got}] | cosine: {cosine}") 
	return cosine

