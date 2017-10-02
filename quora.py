import os
import webbrowser
import sys
from colorama import Fore, Back, Style
from colorama import init
init()
#os.environ["HTTPS_PROXY"] = "http://username:pass@192.168.1.107:3128"
import requests
from bs4 import BeautifulSoup
import time

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


#Take query and convert into search parameter
#query=input('Ask your Quora que: ')
arg = sys.argv
query = ''
for i in range(1,len(arg)-2):
    query=query+arg[i]
    query=query+'+'
print(query)
#retrieve query

url='https://www.quora.com/search?q='+query
source_code = requests.get(url, headers=headers, timeout=15)
plain_text=source_code.text
soup=BeautifulSoup(plain_text,"html.parser")

#get the relevant questions list
que_list=soup.findAll('a',{'class':'question_link'})

hrefs=list(que_list)
#convert into user-friendly string
print(Fore.GREEN+'            <<  Showing some relevant questions asked  >>')
for i in range(len(que_list)):
    que_list[i]['href']=que_list[i]['href'].replace('-',' ')
    que_list[i]['href']=que_list[i]['href'].replace('/','')
    print(str(i+1)+'. '+que_list[i]['href'])
print('         <-------------------------------/-------------------------------->')
#get_inp=input('Select a question from the above > ')
get_inp = arg[len(arg)-2]
#retrieve the page with that answer
url='https://www.quora.com/'+hrefs[int(get_inp)-1]['href'].replace(' ','-')
try:
    source_code = requests.get(url, timeout=15)
    plain_text=source_code.text
    soup=BeautifulSoup(plain_text,"html.parser")
    ans=soup.findAll('div',{'class':'AnswerHeader ContentHeader'})
    header=ans[0].text
    nans=ans[0].parent
    mans=nans.next_sibling
    #man=mans.findNextSibling()
    text=mans.text
    pos=text.find('Upvotes')
    uf=text[0:pos+7]
    print(Fore.BLUE+header)
    print(uf)
except Exception as e:
    print(e)
    print('Sorry, this que hasn\'t been answered.')
print('        <----------------------------------/------------------------------->')
#a=input('Head over to the link for more answers?(y/n) ')
a= arg[len(arg)-1]
if a is 'y':
    webbrowser.open(url)
    time.sleep(2)
    exit()
