from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions
import pandas as pd


natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='34qzJpNfbmmav0ZFkGM9vM_enLCTAOuQsd5s4odeF19l',
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api'
)

keywords = {"quake", "earth", "shake", "tremble"}

    # takes in a twitter text in the form of a string and 
    # creates a row with information such as if it contains the keyword
    # 'quake' and columns on sadness, joy, fear, disgust, and, anger
def constructRow(text, keywords, isEarthquake):
    
    
    try:
        response = natural_language_understanding.analyze(
                html=text,
                features=Features(emotion=EmotionOptions())).get_result()
    
        dictionary = response["emotion"]["document"]["emotion"]
    # going to remove the ones with only 0's   
    except:
        dictionary = {"anger" :0,
                      "disgust": 0,
                      "fear": 0,
                      "joy": 0,
                      "sadness": 0}
    
    for keyword in keywords:
        columnName = "hasSubstring_" + keyword
        # find() returns index of location of keyword, and -1 
        # if none, so I changed it into true/ false
        dictionary[columnName] = text.lower().find(keyword) >= 0
    dictionary["duringEarthquake"] = isEarthquake    
    
    return pd.Series(dictionary)



# Dataset with good number of earthquake tweets
tweets = pd.read_json("SF_2014-08-24.json")
earthquakeTweets = tweets.iloc[12000:13306]     # The beginning of the earthquake(earthquake only tweets)
nonEarthquake = tweets.iloc[13307:15000]        # Before the earthquake(non earthquake tweets)

    
dataframe = pd.DataFrame()
i = 0
for index, row in earthquakeTweets.iterrows():
    dataframe = dataframe.append(constructRow(row["text"], keywords, True), ignore_index = True)    # isEarthquake column = True
    
for index, row in nonEarthquake.iterrows():
    dataframe = dataframe.append(constructRow(row["text"], keywords, False), ignore_index = True)   # isEarthquake column = False

for index, row in dataframe.iterrows():
    if (row["anger"] == 0 and row["disgust"] == 0 and row["fear"] == 0 and row["joy"] == 0 and row["sadness"] == 0):
        dataframe = dataframe.drop(index)
        
        
import numpy as np
import matplotlib.pyplot as plt

# pretend that 'duringEarthquake' variable is our dependant vraibles
Y = dataframe.iloc[:, 2:3].values

# the rest are independant variables
X = dataframe.drop(labels = "duringEarthquake", axis=1)



# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


















