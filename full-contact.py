from fullcontact import FullContact
import json
fc = FullContact('your_api_key')
user_id = input('Please enter user email-id: ')
r = fc.person(email=user_id)
#data = json.load(r.json())
data = r.json()
#print(data['contactInfo'])

if data['status']==200:
    print('Name: '+data['contactInfo']['fullName'])
    print('Location: '+data['demographics']['locationDeduced']['deducedLocation'])
else:
    print('Data unavailable right now.')
