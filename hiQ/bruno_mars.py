import os
import requests

from bs4 import BeautifulSoup
# uncomment the line below and set your user_id n pass if working on college proxy
# os.environ["HTTPS_PROXY"] = "https://user_id:pass@192.168.1.107:3128"

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
url='https://en.wikipedia.org/wiki/Bruno_Mars'

source_code = requests.get(url, headers=headers, timeout=5)  # get the raw code
plain_text = source_code.content  # convert into plain text
soup = BeautifulSoup(plain_text,"html.parser")  # convert to a bs4 object

name = soup.find('h1',{'id':'firstHeading'})
nickname = soup.find('span',{'class':'nickname'})
print ('Name: {}'.format(name.get_text()))
print ('Nickname: {}'.format(nickname.get_text()))
paras = soup.find_all('p')
print (paras[0].get_text())
