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


# some required datas to initialize with
imaplib._MAXLINE = 400000

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "inboxmeabhinav" + ORG_EMAIL
FROM_PWD = getpass.getpass()
SMTP_SERVER = "imap.gmail.com"  # varies depending on the imap server
SMTP_PORT = 993

i = 0
body_fetched = []  # to contain all the lines which has been printed already


def main():
    global i, body_fetched, email_message
    clear()
    # login
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.list()
    mail.select('inbox')
    inp = 'n'

    # start fetching mails one by one
    while (inp != 'q'):
        print('Fetching mails. Please wait...')
        if inp == 'n':
            i += 1
        elif inp == 'p' and i != 1:
            i -= 1
        else:
            print('Please enter valid input.')

        result, data = mail.uid('search', None, "ALL")  # search and return uids instead
        latest_email_uid = data[0].split()[-i]  # fetch mails
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)

        clear()  # clear screen and print mail
        print 'To:', email_message['To']
        print 'Sent from:', email_message['From']
        print 'Date:', email_message['Date']
        print 'Subject:', email_message['Subject']
        print '\n'
        maintype = email_message.get_content_maintype()

        if maintype == 'multipart':  # get the body of the mail
            body = email_message.get_payload()[0].get_payload()  # to get the plain text only
        elif maintype == 'text':
            body = email_message.get_payload()[0]
        
        # print body.split('\n')
        # preprocessing the body to remove signature
        body = remove_signature(body)
        # print body
        body_fetched = []

        dols = extract_dol(body)
        phone_no = get_phoneNumber(body)

        # adding the two items in the fetched list
        body_fetched.extend(phone_no.split('\n'))
        body_fetched.extend(dols)

        # print body_fetched
        print 'Phone Number: ', phone_no

        # print body_fetched

        for dol in dols:
            print str(dol)

        print '\n'
        # print body_fetched
        remaining_body_location = remaining_msg(body.split('\n'), body_fetched)
        # print remaining_body_location

        location = fetch_address(remaining_body_location)

        if len(location) != 0:
            for address in location:
                body_fetched.append(str(address))
                print 'Address: ', address
        else:
            loc = location_fetch(remaining_body_location)
            body_fetched.append(str(loc))
            loc = loc.split()
            new_locs = []
            for lo in loc:
            	if 'ADDRESS' not in lo.upper():
            		new_locs.append(lo)
            # print 'didn\'t work'
            print 'Address: ', ' '.join(new_locs)

        # print 'fetched ', body_fetched
        remaining_body_name = remaining_msg(remaining_body_location, body_fetched)
        # print 'name ', remaining_body_name
        names = extract_names(remaining_body_name)

        print '\n'

        # if first line contains DAVID ignore it.
        print 'Name: ',
        if len(remaining_body_name) != 0:
	        if 'DAVID' in remaining_body_name[0].upper():
	            names.remove('DAVID')
        for j in range(len(names)):
            print names[j]

        # print '*'*69
        welcome()
        inp = raw_input('>> Enter your choice: ').lower()


# extract DOLs
def extract_dol(body):
    '''splitting the message into lines
	and extracting the lines with DOL in it
	'''

    dol_matches = ['DOL', 'DATE OF LOSS', 'DATE OF ACCIDENT']
    body = body.split('\n')
    dol_arr = []
    for line in body:
        for dol in dol_matches:
            if dol in line.upper():
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
    regex = re.compile(r"\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b")
    for phoneNumber in get_phoneNumbers(text, regex):
        phone_number = phone_number + phoneNumber + "\n"
    return phone_number


def get_phoneNumbers(s, regex):
    ''' returns all the phone numbers present
	in the input string
	'''

    return (phoneNumber for phoneNumber in re.findall(regex, s))


def remaining_msg(msg, fetched):
    '''to return a list of the message
    lines that hasn't been printed yetq
    '''

    # msg = msg.split('\n')
    remains = []  # to contain the remaining body
    # print remains
    try:
        msg = [x.strip() for x in msg]
        fetched = [x.strip() for x in fetched]
        msg = list(filter(lambda a: a != '', msg))
        fetched = list(filter(lambda a: a != '', fetched))
    except:
    	msg = [str(x) for x in msg]
        fetched = [str(x) for x in fetched]
        msg = list(filter(lambda a: a != '\r', msg))
        fetched = list(filter(lambda a: a != '\r', fetched))

    # print 'fetched ', fetched
    for fline in fetched:
        for line in msg:
            try:
                if line.find(fline) != -1:
                    remains.append(line)
                    break
            except:
                pass

    for line in msg:
        for fline in fetched:
            try:
                if fline.find(line) != -1:
                    # print 'line: ', line
                    remains.append(line)
                    break
            except:
                pass

    #print remains
    #print '\n', msg
    for line in remains:
        try:
            msg.remove(line)
        except:
            pass
    return msg


def location_fetch(msg):
    ''' the location ends with either state name or PIN
    using that this function checks for the words in each line
    if it contains the state then it will return the line
	'''
    locs = []
    for line in msg:
        linen = line.upper()
        if linen.find('ADDRESS') != -1:
            locs.append(line)
            break
    for line in msg:
        words = line.split()
        for word in words:
            if word in states:
                locs.append(line)
    return ' '.join(locs)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def welcome():
    print '\n'
    print '>> Enter \'n\' to check NEXT mail'
    print '>> Enter \'p\' to check PREVIOUS mail'
    print '>> Enter \'q\' to QUIT'


if __name__ == '__main__':
    main()
