import re

def get_phoneNumber(text):
  phone_number = ""
  regex = re.compile(r"\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b")
  for phoneNumber in get_phoneNumbers(text, regex):
    phone_number = phone_number + phoneNumber + "\n"
  return phone_number

def get_phoneNumbers(s, regex):
  return (phoneNumber for phoneNumber in re.findall(regex, s))

text = '''
(818) 212-8948
DOL: 10/20/2017 & DOL: 6/2017
10906 woodley ava granada hills CA
(818) 212-8999
Client has two cases to sign
'''
print get_phoneNumber(text)
