import os
import requests
import pyttsx
import time
from bs4 import BeautifulSoup

def speak(value):
    engine = pyttsx.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[4].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-30)
    engine.say(value)
    engine.runAndWait()

url='http://www.cricbuzz.com/'
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


def match():
        source_code = requests.get(url, headers=headers, timeout=5)
        plain_text=source_code.text
        soup=BeautifulSoup(plain_text,"html.parser")



        link=soup.find('div',{'class':'cb-ovr-flo cb-hmscg-tm-nm'})
        team=link.string

        link2=soup.findAll('div',{'class':'cb-ovr-flo'})
        score=link2[2].string

        link3=soup.findAll('div',{'class':' cb-ovr-flo cb-text-live'})
        required=link3[0].string
        
        print team+' '+score
        print required
        speak(team+'scored'+score)
        speak(required)

while(1):
    match()
    time.sleep(30)
