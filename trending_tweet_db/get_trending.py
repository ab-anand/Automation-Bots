#!/usr/bin/python

try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from keys import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET
import sqlite3

conn = sqlite3.connect('tweet_db.db')

conn.execute('''DROP TABLE IF EXISTS TWEETS;''')

conn.execute('''CREATE TABLE IF NOT EXISTS TWEETS
         (ID INT PRIMARY KEY     NOT NULL,
         screen_name  TEXT    NOT NULL,
         tweet_time            TEXT     NOT NULL,
         favorite_count        INT,
         query				   TEXT,
         retweet_count         INT)
         ;''')

# print ACCESS_TOKEN, ACCESS_SECRET
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter = Twitter(auth=oauth)

# get the trending topics in India
sfo_trends = twitter.trends.place(_id = 23424848)


# print json.dumps(sfo_trends, indent=4)
# print len(sfo_trends[0]['trends'])
length = len(sfo_trends[0]['trends'])
topics = [sfo_trends[0]['trends'][i]['name'] for i in range(length)]
print topics
pk = 1
for topic in topics:
	tweet = twitter.search.tweets(q=topic, result_type='recent', lang='en', count=1)
	try:
		screen_name = tweet['statuses'][0]['user']['screen_name']
	except:
		continue
	tweet_time = tweet['statuses'][0]['created_at']
	try:
		favorite_count = tweet['statuses'][0]['retweeted_status']['favorite_count']
	except KeyError:
		favorite_count = 0
	retweet_count = tweet['statuses'][0]['retweet_count']
	query = tweet['search_metadata']['query']
	# print query, screen_name, tweet_time, favorite_count, retweet_count
	row = (pk, screen_name, tweet_time, favorite_count,	query, retweet_count)
	conn.execute('''INSERT INTO TWEETS (ID, screen_name, tweet_time, favorite_count, query, retweet_count) 
					VALUES (?, ?, ?, ?, ?, ?)''', row)
	conn.commit()
	pk += 1
	print 'done'
       
conn.close()