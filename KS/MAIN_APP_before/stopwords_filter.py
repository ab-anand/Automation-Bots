from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))  # setting the language


def process_names(body):
	'''takes a input list of body
	and removes all the stopwords
	'''
	new_body = []

	for line in body:
		word_tokens = word_tokenize(line)  # tokenize the string

		filtered_sentence = [w for w in word_tokens if not w in stop_words]  # filtering the words
		line = ' '.join(line)
		new_body.append(line)

	return new_body


# ** Just a test case **
a = ['This', 'is', 'a', 'sample', 'sentence', ',', 'showing', 
'off', 'the', 'stop', 'words', 'filtration', '.']

