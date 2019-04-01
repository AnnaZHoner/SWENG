#Import the necessary methods from tweepy library
import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self, api=None):
        super(StdOutListener, self).__init__()
        self.num_tweets = 0
        self.file = open("tweets.json", "w")
    def on_data(self, data):
        tweet = json.loads(data)
        if (not tweet["retweeted"]) and ('RT @' not in tweet["text"]):
            self.file.write(json.dumps(tweet["user"]["location"]) + ',' + json.dumps(tweet["text"]) + '\n')
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, tweet_mode = "extended", lang = 'en')

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['quake', 'earthquake', 'shaking', 'ground'])
