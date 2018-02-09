import os
import requests
import webbrowser
from bs4 import BeautifulSoup

# uncomment the line below and set the user_id n pass if working on college proxy
# os.environ["HTTPS_PROXY"] = "https://user_id:pass@192.168.1.107:3128"


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
song_name_raw = input('Please enter a song name: ')
song_name = song_name_raw.replace(' ', '%20')
url = 'https://gaana.com/search/{}'.format(song_name)
source_code = requests.get(url, headers=headers, timeout=5)
plain_text = source_code.content
soup = BeautifulSoup(plain_text,"html.parser")
links = soup.find_all('a',{'class':'rt_arw'})
# print (links[0]['href'])
webbrowser.open(links[0]['href'])


