#Import the necessary methods from tweepy library
from cloudant.client import Cloudant
import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from flask import Flask
import os

#initialise application
app = Flask(__name__, static_url_path='')

#retrieve credentials
with open('test_cloudant.json') as c_cred:
        data = json.load(c_cred)
        username = data['username']
        password = data['password']
        url = data['url']
        account_name = username


with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_token = info['ACCESS_KEY']
    access_token_secret = info['ACCESS_SECRET']

client = Cloudant(username, password, url=url, account=account_name, connect=True)

session = client.session()

#initialise port
port = int(os.getenv("PORT"))


class StdOutListener(StreamListener):
    #def __init__(self, api=None):
    #    super(StdOutListener, self).__init__()
    #    self.num_tweets = 0
    #    self.file = open("tweets_word.json", "w")
    def on_data(self, data):
        #db = client['my_database']
        db = client['raw_tweets']
        #self.file = open("tweets_san_francisco.json", "a")
        tweet = json.loads(data)
        if ('extended_tweet' in tweet):
            data_dump = {"created_at" : tweet['created_at'], 'location' : tweet['user']['location'] , 'text' : tweet['extended_tweet']['full_text']}
        else:
            data_dump = {"created_at" : tweet['created_at'], 'location' : tweet['user']['location'] , 'text' : tweet['text']}

        if (not tweet["retweeted"]) and ('RT @' not in tweet["text"]):
            db.create_document(data_dump)
            #self.file.write(json.dumps(data_dump) + '\n')
            #self.file.write(json.dumps(tweet['user']['location']) + ',' + json.dumps(tweet['text']) + '\n')
        return True

    def on_error(self, status_code):
        print('Encountered error with status code:' + str(status_code))
        return True #not killing stream

    def on_timeout(self):
        print('Timeout...')
        return True # not killing stream


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track=['quake', 'earthquake', 'temblor', 'tremor', 'aftershock', 'magnitude', 'seismic', 'seismology', 'epicentre'], languages = ['en'])
    #west, south is minus
    #stream.filter(locations=[-122.75,36.8,-121.75,37.8,-74,40,-73,41])#San Francisco or New York
    app.run(host='0.0.0.0', port=port)
