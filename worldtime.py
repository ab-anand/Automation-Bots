import pytz
import datetime
import argparse
from timezonefinder import TimezoneFinder
from pygeocoder import Geocoder

# Read command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--location", 
                    help="target location", 
                    type=str, metavar="", default="")
args = parser.parse_args()

if args.location != "":
    location = args.location.decode('utf8')
    # Obtain longitude, latitude via Geocoder
    result = Geocoder.geocode(location)
    coordinate = result[0].coordinates
    location = ", ".join([result[0].city, result[0].country])
    # Fetch Timezone by longitude, latitude via timezonefinder
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lat=coordinate[0], lng=coordinate[1])
else:
    # Use IP address to get physical position
    import urllib2
    import json

    result = urllib2.urlopen('http://freegeoip.net/json/')
    json_string = result.read()
    location = json.loads(json_string)
    timezone = location['time_zone']
    location = ", ".join([location['city'], location['country_name']])
    result.close()

# Get Time via pytz
time = datetime.datetime.now(pytz.timezone(timezone))
print("%s %s" % (location, str(time).split('.')[0]))