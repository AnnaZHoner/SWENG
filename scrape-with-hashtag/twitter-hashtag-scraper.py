# -*- coding: utf-8 -*-

import tweepy
import csv
import json

# Twitter API credentials
with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']

# Create the api endpoint

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# The maximum number of tweets to extract

tweets_to_extract = int(input('Number of tweets to extract: '))

# The hashtag to search for

hashtag = input('Hashtag to scrape: ')

#o Open/Create a file to write to
write_file = open('tweets_with_' + hashtag + '.csv', 'w')
# use csv writer
csv_writer = csv.writer(write_file)

for tweet in tweepy.Cursor(api.search, q = '#' + hashtag, tweet_mode = 'extended', lang = 'en').items(tweets_to_extract):
    #print(tweet.created_at, tweet.full_text)
    csv_writer.writerow([tweet.created_at, tweet.full_text.encode('utf-8')])
