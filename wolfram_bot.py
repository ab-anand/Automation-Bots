#created by Abhinav Anand

import wolframalpha

query=raw_input('Ask me something: ')
app_id='API_KEY'


client=wolframalpha.Client(app_id)

def wolfram(query):
    res=client.query(str(query))
    try:
       ans=next(res.results).text
    except:
       ans='Sorry, I don\'t know that.'
    return ans

print wolfram(query)

q='y'
while q=='y':
   q=raw_input('Wanna ask another question(y/n)? ')
   if q=='n':
       break
   elif q=='y':
       query=raw_input('You: ')
       print 'Bot: '+wolfram(query)
   else:
       print 'Invalid input. Please try again'
       q='y'
       
       
        
    


