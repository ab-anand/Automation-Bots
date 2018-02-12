from talon.signature.bruteforce import extract_signature
text = '''(818) 212-8948
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
text, signature = extract_signature(text)
print text

