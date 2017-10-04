# A fun little crawler to see how many steps are between two articles.
# Uses only standard libraries.
# Note: Will most likely not take the same path twice.

import re
import urllib.request
from time import sleep
from random import randint

def Main(x, y):
    z = urllib.request.urlopen('https://wikipedia.org/wiki/' + x).read()
    z = z.decode('utf-8')
    f = re.findall(
            r'<a href="/wiki/(?!Help\:|Special:|Wikipedia:|Portal:|File:)(.*?)"',
        z)
    if y in f:
        print('Found %s in: https://wikipedia.org/wiki/%s' %(y, x))
    else:
        print('%s not found in https://wikipedia.org/wiki/%s' %(y, x))
        sleep(1) # Sleep so you're not overloading the server with requests.
        r = randint(0, len(f) - 1)
        Main(f[r], y)

if __name__ == '__main__':
    x = input('Topic to start: ')
    y = input('Topic to end: ')
    Main(x, y)
