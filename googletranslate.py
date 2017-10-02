import argparse
import requests
import urllib
import re

# Declare source text, source language 
# and target language variables
sourceText = "" 
sourceLang = ""
targetLang = ""

# Read command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-st", "--sourcetext", help="source text", type=str, metavar="")
parser.add_argument("-sl", "--sourcelanguage", help="source language; Default value: auto", 
                    type=str, default="auto", metavar="")
parser.add_argument("-tl", "--targetlanguage", help="target language; Default value: en",
                    type=str, default="en", metavar="")
args = parser.parse_args()
print args
sourceText = args.sourcetext.decode("utf8")
sourceLang = args.sourcelanguage.decode("utf8")
targetLang = args.targetlanguage.decode("utf8")

# invoke google translate
url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" \
        + sourceLang + "&tl=" + targetLang + "&dt=t&q=" + urllib.quote(sourceText.encode('utf8'))
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
sc = requests.get(url, headers=headers)

translatedText = re.findall(r'"([^"]*)"', sc.text)[0]
print "Source Text: " + sourceText
print "Translation: " + translatedText