#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyap

test_address = """  
 David,

We need a witness statement for one of our files.  Please see below for
the list of questions.

Witness name: Salina Ramos
Phone: (818) 723-6578


Sincerely, 

Jackie Levine
Assistant to Kyle K. Madison



11111 Santa Monica Blvd, Suite 100
Los Angeles, CA 90025
(310) 201-7676 (Office)
(310) 744-0111 (Fax)

The information in this e-mail (including attachments, if any) is
considered confidential and is intended only for the recipient(s) listed
above. Any review, use, disclosure, distribution or copying of this e-mail
is prohibited except by or on behalf of the intended recipient. If you
have received this email in error,
    """
test = '''
Hi David, 

Please send someone to sign:

Maria Reyes
Ph: 909-246-5391 (SPANISH)
Address: 4138 Mission Blvd Space 58, Montclair, CA 91763
DOL 01/08/2018

Thank you


'''
t2 = '''
Hello Team,
 
We have a family that was involved in a MVA and needs to be contacted to set up an appointment for tomorrow, clients prefer at 11:00 a.m.
 
Here is the contact person/client and location of sign-up, please note adult clients areSpanish speaking only:
 
Jose A. Rios   
*400 Palm Avenue*
*Watsonville, CA 95076*
(831) 234-3634
 
Date of Accident:  12/17/17
 
Clients:
 
1.	Juan R. Vega – driver
2.	Jose A. Rios – passenger & vehicle owner
3.	Enriqueta Rios – passenger & wife to Jose Rios
4.	Elizabeth Rios – passenger & daughter to Jose Rios [she has down syndrome, Jose Rios will be her legal guardian and will answer questions on her behalf]
5.	Roxanna Rios – passenger & granddaughter to Jose Rios [she is a minor, Pedro Rios is the father]
6.	Iliana Rios – passenger & granddaughter to Jose Rios [she is a minor, Pedro Rios is the father]
 
All adult clients will be at the above address, we are waiting to confirm if the father of both minors will be present, if not a separate meeting will be necessary. 
 
'''
t3 = '''
Jose A. Rios
*400 Palm Avenue*
*Watsonville, CA 95076*
'''
def preprocess(arr_body):
    new_arr = []
    for line in arr_body:
        line = line.replace('*', '')
        new_arr.append(line)
    return new_arr

def fetch_address(arr_body):
	msg_body = preprocess(arr_body)
	msg_body = '\n'.join(msg_body)
	# print msg_body
	addresses = pyap.parse(msg_body, country='US')
	location = []
	try:
		for address in addresses:
		        # shows found address
				location.append(address)
				# print address	
	except:
		pass
	return location

#print(address.as_dict())
# print fetch_address(t3)
