text = """ 
Annette Anderson,

I need this signed up ASAP in Santa Cruz. Brain injury. Wi


Tel#: 831-201 7096

Needs a call right now to schedule time and location

Reza


-- 

Reza Torkzadeh 
Office: 888.222.8286
Mobile: 949.698.8087

Please note: This message is being sent via mobile phone. Please excuse any informalities, brevity, spelling and grammatical errors.
"""

from nameparser import HumanName
name = HumanName(text)
print name.full_name
