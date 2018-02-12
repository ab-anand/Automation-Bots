import talon
from talon import signature as sig
from talon.signature.bruteforce import extract_signature
# don't forget to init the library first
# it loads machine learning classifiers
talon.init()

# text1, text2, text3 are test cases which can used in debugging otherwise they ain't use in our app
text1 = '''(818) 212-8948
DOL: 10/20/2017 & DOL: 6/2017
10906 Woodley Ave Granada Hills CA 
Client has two cases to sign
 
--
Leslie Garcia, Intake Coordinator
Akiva Niamehr LLP
10900 Wilshire Blvd. Ste. 930 | Los Angeles, CA 90024
P: 424.653.1093 | F: 310.882.5444
E: leslie@anattorneys.com
'''
text3 = '''
Hi David,

 

We need a witness statement for one of our files.  Please see below for

the list of questions.

 

Witness name: Salina Ramos

Phone: (818) 723-6578




-- 
Abhinav Anand,
+91 8461077468
ABV-IIITM, GWALIOR, MP, 474015
'''
text2 = """Annette Anderson,
11833 Spring Laurel DR
Charlotte, NC 28215
704-724-4697
 
Client is a referral from our chiro- she is there now about to have her appointment. Please reach out in the next hour!
 
Respectfully,

Lacie N. Johnson
Intake Paralegal 
Law Offices of Shane Smith, PC
263 Hwy 74 N
Peachtree City, GA 30269

770.487.8999 ext. 42
770.631.7667 fax
"""

def remove_signature(message):
	'''takes the message as string 
	and returns a string removing signature 
	'''
	msge = message.split('\n')  # break the message in line
	try: 
		msg = [x.rstrip() for x in msge]  # remove the white spaces
	except:  
		pass # otherwise proceed 
	message = '\n'.join(msg)  # form a string from the msg list

	if '--' in msg:  # method 1 by checking the occurence of '--' in msg list
		text, signature = extract_signature(message)  # extract the filtered text and signature
	else:  #METHOD 2 by using ML way
		text, signature = sig.extract(message, sender='john.doe@example.com')  # extract the text and signature, the sender argument is necessary but any fake email id can be used

	return text

	 
# print remove_signature(text1)
# print '\n\n'
# print remove_signature(text3)
