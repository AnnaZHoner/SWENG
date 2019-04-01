import pandas as pd
import json

import time

tweets = pd.read_json("SF_2014-08-24.json")

# 13304 to 12572
# 3 minutes worth of tweets after an earthquake
relevantTweets = tweets.iloc[12572:13304]
#13279
relevantTweets.drop(13279, inplace=True)
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
alarmThreshold = 28

alerted = False

for index, row in relevantTweets[::-1].iterrows():
    time.sleep(0.5)
    tweets.append(row['text'])
    if 'earthquake' or 'quake' in row['text']:
        numberContainKeyword = numberContainKeyword + 1
    else:
        numberNotContainKeyword = numberNotContainKeyword + 1
    print("Tweet: " + row['text'])
    print("Analysing " + str(numberContainKeyword + numberNotContainKeyword) + " tweets")
    print(str(numberContainKeyword) + " tweets related to earthquake")
    print(str(numberNotContainKeyword) + " tweets not related to earthquake")
    print("Earthquake Probability: " + str((numberContainKeyword / numberNotContainKeyword) / alarmThreshold))
    print()
# pops off 31'st tweet and adjusts the counter
    if len(tweets) >= 29 :
        if 'earthquake' or 'quake' in tweets.pop():
            numberContainKeyword = numberContainKeyword - 1
        else:
            numberNotContainKeyword = numberNotContainKeyword - 1
            
    if (not alerted) and (numberContainKeyword / numberNotContainKeyword >= alarmThreshold and (numberContainKeyword + numberNotContainKeyword >= 29)):
        # put info in json file 
        # need to make a dictionary with the stats
        #alertData = {"location": location, "distress ratio": numberContainKeyword / numberNotContainKeyword, "tweets": tweets }
        alerted = True
        print("EARTHQUAKE IN SAN FRANSISCO")
        break;
        #with open('alerts.json', 'a') as outfile:
            #json.dump(alertData, outfile)
        