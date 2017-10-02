import sys
import time
import datetime
import requests
import json
from colorama import Fore, init

URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
UPDATES = []

def earthquake_print(data):
    for i in data['features']:
        if i['id'] not in UPDATES:
            UPDATES.append(i['id'])
            print('___________________________________________________________________________________________________')
            print(i['properties']['title'], end=' MAG: ')
            print(Fore.RED+str(i['properties']['mag']))
            print('Location:', i['properties']['place'])
            alert = i['properties']['alert']
            if alert == 'green':
                print(Fore.RED + 'Type: ' + i['properties']['type'], end='  ')
            elif alert == 'yellow':
                print(Fore.YELLOW + 'Type: ' + i['properties']['type'], end='   ')
            else:
                print(Fore.BLUE + 'Type: ' + i['properties']['type'], end='    ')
            ms = i['properties']['time']
            print(datetime.datetime.fromtimestamp(ms/1000.0))
            print('INFO:', i['properties']['url'])
            
def get_earthquakes():
    resp = requests.get(URL)
    resp = json.loads(resp.text)
    count =  resp['metadata']['count']
    if count != 0:
        earthquake_print(resp)
    else:
        pass
    
if __name__ == '__main__':
    init(autoreset=True)
    if len(sys.argv) != 2:
        print('Usage: earthquake.py [time in seconds]')
    else:
        seconds = int(sys.argv[1])
        while True:
            get_earthquakes()
            time.sleep(seconds)
