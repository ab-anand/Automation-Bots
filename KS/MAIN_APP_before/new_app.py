# Reading inbox emails from CLI.
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ == 'abhinav anand'

import base64, imaplib, email, re, os
import getpass

from info import us_states as states
from address import fetch_address
from name import extract_names
from remove_sig import remove_signature 
from filters import (subject_items, phone_items,
					sign_items_post, sign_items_pre
					)
from stopwords_filter import process_names
from dol_extractor import extract_dol

# some constant datas to initialize with
imaplib._MAXLINE = 400000

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "inboxmeabhinav" + ORG_EMAIL
FROM_PWD = getpass.getpass()
SMTP_SERVER = "imap.gmail.com"  # varies depending on the imap server
SMTP_PORT = 993


i = 0  # a counter to to move to next or previous mail
body_fetched = []  # to contain all the lines which has been printed already


def main():
	''' connect with the server
	fetch the mails and do the preprocessing
	'''
	global i, body_fetched, email_message
	clear()  # to clear the screen before fetching the mails
	# login
	mail = imaplib.IMAP4_SSL(SMTP_SERVER)  # connect with the server 
	mail.login(FROM_EMAIL, FROM_PWD)  # loggin in 
	mail.list()  # get a list of mails
	mail.select('inbox')  # getting from the INBOX
	inp = 'n'  # an inital counter for the first mail

	# start fetching mails one by one
	while (inp != 'q'):
		print('Fetching mails. Please wait...')
		if inp == 'n':  # fetch next mail
			i += 1
		elif inp == 'p' and i != 1:  # fetch previous mail, making sure it's not the first mail already
			i -= 1
		else:  # in case user gives some invalid input
			print('Please enter valid input.')

		result, data = mail.uid('search', None, "ALL")  # search and return uids instead
		latest_email_uid = data[0].split()[-i]  # fetch list of mails id
		result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')  # iterate through the email and fetch the email using RFC822 protocol
		raw_email = data[0][1]  # to get raw mails from the data fetched
		email_message = email.message_from_string(raw_email)  # convert it as a string

		clear()  # clear screen and print mail
		print 'To:', email_message['To']  # print TO of the mail
		print 'Sent from:', email_message['From']  # print FROM of the mail
		print 'Date:', email_message['Date']  # print DATE of the mail

		# preprocess the subject to remove unwanted words
		subject = [p.upper() for p in email_message['Subject'].split()]  # break subject into list
		for item in subject_items:  # iterate n delete the unwanted items
			if item in subject:
				try:
					subject.remove(item)
				except:
					pass

		subject  = ' '.join(subject)
		print 'Subject:', subject  # print SUBJECT of the mail
		
		print '\n'
		maintype = email_message.get_content_maintype()  # check the type of mail 

		if maintype == 'multipart':  # get the body of the mail if type is 'multipart'
			body = email_message.get_payload()[0].get_payload()  # to get the plain text only
		elif maintype == 'text':  # get the body if the mail if type is 'text'
			body = email_message.get_payload()[0]
		

		body = remove_signature(body)  # preprocessing the body to remove signature

		body_fetched = []  # to keep the track of things we gonna extract from the body like DOL, phone no.
		dols_in = extract_dol_in(body)
		dols = extract_dol(dols_in)  # extract DOL
		phone_num = get_phoneNumber(body)  # extract phone no

		# removing unwanted keywords from phone no
		phone_no = list(phone_num)
		for item in phone_items:
			if item in phone_no:
				phone_no = list(filter(lambda a: a != item, phone_no))

		phone_no = ''.join(phone_no)

		# adding the items in the body_fetched list
		body_fetched.extend(phone_num.split('\n'))
		body_fetched.append

		print 'Phone Number: ', phone_no

		for dol in dols:  # print the DOLs
			print str(dol)

		print '\n'

		remaining_body_location = remaining_msg(body.split('\n'), body_fetched)  # get the body after removing what we extracted

		location = fetch_address(remaining_body_location)  # extract location

		if len(location) != 0:  # if some location is extracted by ML method
			for address in location:  
				body_fetched.append(str(address))  # add the location to the body_fetched list
				print 'Address: ', address  # print address
		else:  # if no location is extracted then try the brute force
			loc = location_fetch(remaining_body_location)  # extract location
			body_fetched.append(str(loc))  # add it to the list
			loc = loc.split()  # create a list breaking the address line in words
			new_locs = []  # create a list to add the words in location
			for lo in loc:  # if the location line starts with 'ADDRESS' then remove it and add the remaining words in new_locs list
				if 'ADDRESS' not in lo.upper():
					new_locs.append(lo)

			print 'Address: ', ' '.join(new_locs)  # print the location as a string forming from the new_locs list 

		remaining_body_name = remaining_msg(remaining_body_location, body_fetched)  # get the body after removing what we extracted

		# filtering out no of sign/cases
		req_line = ''
		for item in sign_items_pre:
			for part in remaining_body_name:
				if item in part.upper():
					req_line = part
					break

		req_item = ''
		for item in sign_items_post:
			if item in req_line.split():
				req_item = item
				break

		print 'NO OF CASES/SIGNS: ', req_item
		print '\n' 
		try:
			remaining_body_name = process_names(remaining_body_name)  # remove the stopwords
		except:
			pass
			
		names = extract_names(remaining_body_name)  # extract the names from the remaining body

		print '\n'

		
		print 'Name: ',
		if len(remaining_body_name) != 0:  # if there are names extracted
			if 'DAVID' in remaining_body_name[0].upper():  # if first line contains DAVID ignore it.
				names.remove('DAVID') 

		for j in range(len(names)):  # print names
			print names[j]

		welcome()  # print the welcome message 
		inp = raw_input('>> Enter your choice: ').lower()  # take the input for next/previous mails


def extract_dol_in(body):
	'''splitting the message into lines
	and extracting the lines with DOL in it
	'''

	dol_matches = ['DOL', 'DATE OF LOSS', 'DATE OF ACCIDENT']  # creating the possible ways of writing DOLs
	body = body.split('\n')  # create a list based on the every next line
	dol_arr = []  # create a list to add the DOL if there is any in the list
	for line in body:  
		for dol in dol_matches: 
			if dol in line.upper():  # if any DOL or similar words are there in body then add it to the list
				dol_arr.append(line)
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
	present in the text 
	'''

	phone_number = ""  
	regex = re.compile(r"\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b")  # regex to match the pattern of phone no
	for phoneNumber in get_phoneNumbers(text, regex):  # get a list of all phone no present present using function get_phoneNumbers
		phone_number = phone_number + phoneNumber + "\n"  # create a string of phone no from the list returned
	return phone_number


def get_phoneNumbers(s, regex):
	''' returns all the phone numbers present
	in the input string
	'''
	return (phoneNumber for phoneNumber in re.findall(regex, s))  # using the regex provided in function get_phoneNumber extract all phone no


def remaining_msg(msg, fetched):
	'''to return a list of the message
	lines that hasn't been printed yet
	msg - list that is our mail body
	fetched - list that has been fetched and which needs
	to be removed from msg list

	----  LOOP 1 description  ----
	ex- suppose we fetched 'Ram' from 'Ram is going to school'.
	So 'Ram'(element in fetched list) is a small part of 'Ram is going to school'(element in msg list).
	Hence fetched list element is smaller than or just a small part of msg list elements. 
	Hence LOOP 1 checks for every such element in fetched list and helps to remove it from msg list

	----  LOOP 2 description  ----
	ex - Suppose we fetched "3055 Wilshire Blvd., 12th Floor Los Angeles, CA  90010"  from
	msg list "3055 Wilshire Blvd., 12th Floor" , "Los Angeles, CA  90010"
	Clearly fetched element is combination of two elements of msg list and hence bigger than
	both the elements so LOOP 2 searches for msg list elements(smaller) from the fethced list 
	elements(bigger) and helps to remove it.
	'''

	remains = []  # to contain the lines that need to be removed

	try:
		msg = [x.strip() for x in msg]  # to remove the whitespaces from msg list
		fetched = [x.strip() for x in fetched]  # to remove the whitespaces from fetched list
		msg = list(filter(lambda a: a != '', msg))  # to filter out '' kinda strings remained in msg list
		fetched = list(filter(lambda a: a != '', fetched))  # to filter out '' kinda strings remained in fetched list
	except:  # if there is no whitespaces
		msg = [str(x) for x in msg]  # first convert the raw msg list elements as string
		fetched = [str(x) for x in fetched]  # convert the raw fetched list elements as string
		msg = list(filter(lambda a: a != '\r', msg))  # filter out '\r' kinda elements in msg list
		fetched = list(filter(lambda a: a != '\r', fetched))  # filter out '\r' kinda elements in msg list

	for fline in fetched:  # check above for LOOP 1 description
		for line in msg:
			try:
				if line.find(fline) != -1:  # if msg list contains any fetched list elements
					remains.append(line)  # add it to the remains list
					break
			except:  # if not contains then simply continue the loop
				pass

	for line in msg:  # check above for LOOP 2 description
		for fline in fetched:
			try:
				if fline.find(line) != -1:  # if fetched list contains any msg list elements 
					remains.append(line)  # add it to the remains list
					break
			except:  # otherwise continue
				pass

	#print remains
	#print '\n', msg

	for line in remains:
		try:
			msg.remove(line)  # now delete all the elements that we added in remains element
		except:
			pass  # otherwise simply continue the loop
	return msg


def location_fetch(msg):
	''' the location ends with either state name or PIN
	using that this function checks for the words in each line
	if it contains the state then it will return the line
	'''
	locs = []  # to add location if there is any
	for line in msg:
		linen = line.upper()
		if linen.find('ADDRESS') != -1:  # check the line if it starts with 'ADDRESS' ex- 'ADDRESS: Los Angeles, CA  90010'
			locs.append(line)  # include the line
			break
	for line in msg: 
		words = line.split()  # divide the msg lines into words
		for word in words:
			if word in states:  # check if the words contains any US states name which is present in info.py file
				locs.append(line)  # add the line
	return ' '.join(locs)  # return the line as string 


def clear():
	os.system('cls' if os.name == 'nt' else 'clear')  # to refresh the screen i.e makes the screen blank


def welcome():
	'''shows the navigation menu for the tool'''
	print '\n'
	print '>> Enter \'n\' to check NEXT mail'
	print '>> Enter \'p\' to check PREVIOUS mail'
	print '>> Enter \'q\' to QUIT'


if __name__ == '__main__':
	main()  # run the file
