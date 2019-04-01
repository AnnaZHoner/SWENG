import pandas as pd
import json

tweets = pd.read_json("SF_2014-08-24.json")

# 13304 to 12572
# 3 minutes worth of tweets after an earthquake
relevantTweets = tweets.iloc[12572:13304]

# Process tweets
# Need to pass a thread/object info 
# The object keeps stats on the state of its location(each object is based on location)
# The ghetto version of the state will be a ratio between tweets containing 
# the keyword 'earthquake' and tweets that don't contain it.
location = "San Fransisco, CA"
numberContainKeyword = 0
numberNotContainKeyword = 1
tweets = []
numberOfNewestTweetsToLookAt = 30
# if there are 3 tweets containing "earthquake" to 1 not containing, it will trigger the alert
alarmThreshold = 0.5

alerted = False

for index, row in relevantTweets.iterrows():
    tweets.append(row['text'])
    if 'earthquake' in row['text']:
        numberContainKeyword = numberContainKeyword + 1
    else:
        numberNotContainKeyword = numberNotContainKeyword + 1
    
# pops off 31'st tweet and adjusts the counter
    if len(tweets) >= 30 :
        if 'earthquake' in tweets.pop():
            numberContainKeyword = numberContainKeyword - 1
        else:
            numberNotContainKeyword = numberNotContainKeyword - 1
            
    if (not alerted) and (numberContainKeyword / numberNotContainKeyword >= alarmThreshold and (numberContainKeyword + numberNotContainKeyword > 29)):
        # put info in json file 
        # need to make a dictionary with the stats
        alertData = {"location": location, "distress ratio": numberContainKeyword / numberNotContainKeyword, "tweets": tweets }
        alerted = True
        with open('alerts.json', 'a') as outfile:
            json.dump(alertData, outfile)
     

"""
file = open("sampleTweets.txt","a") 
for index, row in relevantTweets.iterrows():
     file.write( str(str(row['timestamp']).encode("utf-8")) + " " + str(str(row['text']).encode("utf-8")))
     file.write("\n")
     
file.close()
"""
