from cleverwrap import CleverWrap
import pyttsx
import os
os.environ["HTTPS_PROXY"] = "http://ipg_2015003:abhi%4098@192.168.1.107:3128"

cw = CleverWrap("CC1e4meQiePYWnw2-OLoyZ9zcLw")


a='y'
engine = pyttsx.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[4].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-30)
engine.say('Hellllllo there. I\'m scarlett')
engine.runAndWait()
while a is not 'n':
    
    ans=cw.say(raw_input('You: '))
    print 'Kiara: '+ans
    engine.say(ans)
    engine.runAndWait()

    #a=raw_input('wanna chat more(y/n): ')

cw.reset()
