import re
import nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')

document=""" 
David,

I need this signed up ASAP in Santa Cruz. Brain injury. Wi

Joshua Orosco
Tel#: 831-201 7096

Needs a call right now to schedule time and location

Reza


-- 
Reza Torkzadeh 
Office: 888.222.8286
Mobile: 949.698.8087

Please note: This message is being sent via mobile phone. Please excuse any informalities, brevity, spelling and grammatical errors.
"""
check = ['Annette Anderson,',
         'The client is a referral from our chiro- she is there now about to have her',
         'appointment. Please reach out in the next hour!', 'Respectfully,']

def extract_names(document):
	'''takes a string input and
	print a set of all the names present in it
	'''
	document = '\n'.join(document)
	#print document
	document = ' '.join([i for i in document.split() if i not in stop])
	sentences = nltk.sent_tokenize(document)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	names = []
	for tagged_sentence in sentences:
	    for chunk in nltk.ne_chunk(tagged_sentence):
	        if type(chunk) == nltk.tree.Tree:
	            if chunk.label() == 'PERSON':
	                names.append(' '.join([c[0] for c in chunk]))
            

	names_unique=set(names)
	# print(names_unique)
	my_list = list(name.upper() for name in names_unique)
	return my_list

#print extract_names(check)
