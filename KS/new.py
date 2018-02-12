#Read your inbox email and automate the boring stuff.
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64, imaplib, email, re, os
import getpass
from bs4 import BeautifulSoup
imaplib._MAXLINE = 400000

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "inboxmeabhinav" + ORG_EMAIL
FROM_PWD    = getpass.getpass()
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

mail = imaplib.IMAP4_SSL(SMTP_SERVER)
mail.login(FROM_EMAIL, FROM_PWD)
mail.list()
mail.select('inbox')

result, data = mail.uid('search', None, "ALL") # search and return uids instead
latest_email_uid = data[0].split()[-1]
result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
raw_email = data[0][1]

#### parsing email

email_message = email.message_from_string(raw_email)
print 'To:', email_message['To']
print 'Sent from:', email_message['From']
print 'Date:', email_message['Date']
print 'Subject:', email_message['Subject']
print '*'*30, 'MESSAGE', '*'*30
maintype = email_message.get_content_maintype()
#print maintype

if maintype == 'multipart':
    for part in email_message.get_payload():
            if part.get_content_maintype() == 'text':
                print part.get_payload()
elif maintype == 'text':
    print email_message.get_payload()
print '*'*69

