#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyap
test_address = """
Hi David, 

Please send someone to sign:

Maria Reyes
Ph: 909-246-5391 (SPANISH)
Address: 4138 Mission Blvd Space 58, Montclair, CA 91763
DOL 01/08/2018

Thank you
"""

t2 = '''
Hello Team,
 
We have a family that was involved in a MVA and needs to be contacted to set up an appointment for tomorrow, clients prefer at 11:00 a.m.
 
Here is the contact person/client and location of sign-up, please note adult clients areSpanish speaking only:
 
Jose A. Rios   
400 Palm Avenue
Watsonville, CA 95076
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
 
I will be sending the prepared retainers on this group of clients under separate cover.  Thank you. 
 

'''
t3 = '''
Address: VISTA CALIFORNIA 92081
'''
#print test_address
addresses = pyap.parse(t3, country='US')
for address in addresses:
        # shows found address
	print(address)

#print(address.as_dict())
