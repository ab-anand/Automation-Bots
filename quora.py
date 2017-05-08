import os
from colorama import init
init()
import webbrowser
from colorama import Fore, Back, Style
os.environ["HTTPS_PROXY"] = "http://ipg_2015003:abhi%4098@192.168.1.107:3128"
import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


#Take query and convert into search parameter
query=input('Ask your Quora que: ')
query=query.replace(' ','+')

#retrieve query
url='https://www.quora.com/search?q='+query
source_code = requests.get(url, headers=headers, timeout=5)
plain_text=source_code.text
soup=BeautifulSoup(plain_text,"html.parser")

#get the relevant questions list
que_list=soup.findAll('a',{'class':'question_link'})

hrefs=list(que_list)
#convert into user-friendly string
print('            <<  Showing some relevant questions asked  >>')
for i in range(len(que_list)):
    que_list[i]['href']=que_list[i]['href'].replace('-',' ')
    que_list[i]['href']=que_list[i]['href'].replace('/','')
    print(str(i+1)+'. '+que_list[i]['href'])
print('         <-------------------------------/-------------------------------->')
get_inp=input('Select a question from the above > ')

#retrieve the page with that answer
url='https://www.quora.com/'+hrefs[int(get_inp)-1]['href'].replace(' ','-')
try:
    source_code = requests.get(url, timeout=5)
    plain_text=source_code.text
    soup=BeautifulSoup(plain_text,"html.parser")
    ans=soup.findAll('div',{'class':'pagedlist_item'})
    print(ans[0].text)
except:
    print('Sorry, this que hasn\'t been answered.')
print('        <----------------------------------/------------------------------->')
a=input('wanna head over to the link for more answers?(y/n) ')
if a is 'y':
    webbrowser.open(url)




