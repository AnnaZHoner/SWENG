import pandas as pd

tweets = pd.read_json("SF_2014-08-24.json")

# 13304 to 12572
# 3 minutes worth of tweets after an earthquake
relevantTweets = tweets.iloc[12572:13304 :]
file = open("sampleTweets.txt","a") 
for index, row in relevantTweets.iterrows():
     file.write( str(str(row['timestamp']).encode("utf-8")) + " " + str(str(row['text']).encode("utf-8")))
     file.write("\n")
     
file.close()