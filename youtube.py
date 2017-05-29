import os
import webbrowser
os.environ["HTTPS_PROXY"] = "http://username:pass@192.168.1.107:3128"
import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
query=input('Enter the song to be played: ')
query=query.replace(' ','+')

url='https://www.youtube.com/results?search_query='+query
source_code = requests.get(url, headers=headers, timeout=15)
plain_text=source_code.text
soup=BeautifulSoup(plain_text,"html.parser")

songs=soup.findAll('div',{'class':'yt-lockup-video'})
song=songs[0].contents[0].contents[0].contents[0]
link=song['href']
webbrowser.open('https://www.youtube.com'+link)
