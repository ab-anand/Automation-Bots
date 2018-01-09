# Reading inbox emails from CLI.
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ == 'abhinav anand'

import base64, imaplib, email, re, os
import getpass
from info import us_states as states

# some required datas to initialize with
imaplib._MAXLINE = 400000

ORG_EMAIL   = "@gmail.com" 
FROM_EMAIL  = "inboxmeabhinav" + ORG_EMAIL
FROM_PWD    = getpass.getpass()
SMTP_SERVER = "imap.gmail.com" # varies depending on the imap server
SMTP_PORT   = 993

i = 0

def main():
	global i
	clear()
	# login
	mail = imaplib.IMAP4_SSL(SMTP_SERVER)
	mail.login(FROM_EMAIL, FROM_PWD)
	mail.list()
	mail.select('inbox')
	inp = 'n'

	# start fetching mails one by one
	while(inp!='q'):
		print('Fetching mails. Please wait...')
		if inp == 'n':
			i += 1
		elif inp == 'p' and i != 1:
			i -= 1
		else:
			print('Please enter valid input.')
		result, data = mail.uid('search', None, "ALL") # search and return uids instead
		latest_email_uid = data[0].split()[-i] # fetch mails 
		result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
		raw_email = data[0][1]
		email_message = email.message_from_string(raw_email)

		clear() # clear screen and print mail
		print 'To:', email_message['To']
		print 'Sent from:', email_message['From']
		print 'Date:', email_message['Date']
		print 'Subject:', email_message['Subject']
		#print '*'*30, 'MESSAGE', '*'*30
		print '\n'
		maintype = email_message.get_content_maintype()
		#print maintype

		if maintype == 'multipart': # get the body of the mail
		    body = email_message.get_payload()[0].get_payload() # to get the plain text only
		    dols = extract_dol(body)
		    phone_no = get_phoneNumber(body)

		    print 'Phone Number: ', phone_no

		    # remain = remaining_msg(body, phone_no, dols)
		    loc = location(body)

		    for dol in dols:
		    	print str(dol)

		    print '\n'

		    print 'Location: ',str(loc)

		elif maintype == 'text':
			line = email_message.get_payload()[ 0 ]
			dols = extract_dol(line)
			phone_no = get_phoneNumber(line)
			print 'Phone Number: ', phone_no
			remain = remaining_msg(line, phone_no, dols)

			for dol in dols:
				print str(dol)

			print '\n'

			for re in remain:
				print str(re)
		# print '*'*69
		welcome()
		inp = raw_input('>> Enter your choice: ').lower()

# extract DOLs
def extract_dol(string):
	''' splitting the message into lines 
	and extracting the lines with DOL in it '''
	string = string.split('\n')
	dol_arr = []
	for text in string:
		if "DOL" in text:
			dol_arr.append(text)
	return dol_arr


# extract phone no using regex
def get_phoneNumber(text):
	''' Matches 3334445555, 333.444.5555, 333-444-5555, 
	333 444 5555, (333) 444 5555 and all combinations thereof,
	like 333 4445555, (333)4445555 or 333444-5555. 
	Does not match international notation +13334445555, 
	but matches domestic part in +1 333 4445555. 
	using regex for extracting phone numbers
	then pass that compiled regex to get_phoneNumbers
	function and returns a string of phone numbers
	present in the text '''
	phone_number = ""
	regex = re.compile(r"\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b")
	for phoneNumber in get_phoneNumbers(text, regex):
		phone_number = phone_number + phoneNumber + "\n"
	return phone_number

def get_phoneNumbers(s, regex):
	''' returns all the phone numbers present
	in the input string '''
	return (phoneNumber for phoneNumber in re.findall(regex, s))

def remaining_msg(msg, phone_no, dol):
	''' with a purpose of fetching location
	we simply return whatever is remained in
	the message body'''
	msg = msg.split('\n')
	phone_no = phone_no.split()
	exclude = []
	for line in msg:
		for no in phone_no:
			if no in line:
				exclude.append(line)
	dol = [str(a) for a in dol]
	exclude.extend(dol)
	return [remain for remain in msg if remain not in exclude]

def location(msg):
	''' the location ends with either state name or PIN
	using that this function checks for the words in each line
	if it contains the state then it will return the line'''
	msg = msg.split('\n')
	for line in msg:
		words = line.split()
		for word in words:
			if word in states:
				return line

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def welcome():
    print '\n'
    print '>> Enter \'n\' to check NEXT mail'
    print '>> Enter \'p\' to check PREVIOUS mail'
    print '>> Enter \'q\' to QUIT'   

if __name__ == '__main__':
	main() 
