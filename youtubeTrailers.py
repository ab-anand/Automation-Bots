import requests
import os.path
import sys
import re


def previousTrailers(lang):
	if os.path.exists(lang+".txt"):
		file = open(lang+".txt","r")
	else:
		file = open(lang+".txt","w+")
	fileUrls = file.readlines()
	file.close()
	print "Previous " + lang +" Movie Trailers"
	prevFound = False
	for line in fileUrls:
		prevFound = True
		print line.replace('\n','')
	if(prevFound == False):
		print "No previous " + lang + " Movie Trailers\n"

def newTrailers(lang, url, trailerUrl):
	if os.path.exists(lang+".txt"):
		file = open(lang+".txt","r")
	else:
		file = open(lang+".txt","w+")
	fileUrls = file.readlines()
	file.close()
	found = False
	for line in fileUrls:
		if str(url) in line:
			found = True
	if not found:
		file = open(lang+".txt","a")
		file.write(trailerUrl + url + "\n")
		file.close()
		print trailerUrl + url
		return 1


def trailers(baseUrl, lang):
	html = requests.get(baseUrl + lang).text
	results = re.findall(r'href=\"\/watch\?v=(.{11})', html)
	print("Latest " + lang +  " Movie Trailers")
	newFound = False
	for num in xrange(0,len(results),2):
		val = newTrailers(lang, results[num], trailerUrl)
		if(val == 1):
			newFound = True
	if(newFound == False):
		print "No new " + lang + " Movie Trailers"


if __name__ == '__main__':
	baseUrl = "https://www.youtube.com/results?search_query=latest+trailers+"
	trailerUrl = "https://www.youtube.com/watch?v="
	previousTrailers(sys.argv[1])
	trailers(baseUrl, sys.argv[1])