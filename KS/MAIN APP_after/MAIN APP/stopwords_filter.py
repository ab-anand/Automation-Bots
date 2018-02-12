from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))  # setting the language


def process_names(names):
	'''takes a input list
	and removes all the stopwords
	'''

	line = ' '.join(names)  # create a string out of the list
	word_tokens = word_tokenize(line)  # tokenize the string

	filtered_sentence = [w for w in word_tokens if not w in stop_words]  # filtering the words

	return filtered_sentence


# ** Just a test case **
a = ['This', 'is', 'a', 'sample', 'sentence', ',', 'showing', 
'off', 'the', 'stop', 'words', 'filtration', '.']

