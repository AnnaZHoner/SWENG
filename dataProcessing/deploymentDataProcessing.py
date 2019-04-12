from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

import pickle

# DEFINE LOCATINS IN THIS LIST TO INCLUDE THEM IN DETECTION
locations = ["sanfransisco"]
databases= {}

client = Cloudant.iam("fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix", "AWLmt1r-iqtEeWTDjEC38l320ufQGsFAheg40iutvxcB")
client.connect()
# Create a database for each location
for loc in locations:
    databases[loc] = client.create_database(loc + "_database")


    #begin parsing tweets
# regressor for calculateRelveance()
file = open("textRecognitionModel.sav", 'rb')
relevanceRegressor = pickle.load(file)
file.close()

lastDatabaseIdRead = {}
for location in locations:
    get
    



    #TESTED WORKS
# Other key is "probability"
def getTweetAtIndex(index, location, key = "tweet"):
    client = Cloudant.iam("fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix", "AWLmt1r-iqtEeWTDjEC38l320ufQGsFAheg40iutvxcB")
    client.connect()
    url = "https://fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix:e01ad0f8a3355ea74bf8efeb523cd6da8e8afe94f5a26b2e6af4a7112dd1d144@fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix.cloudantnosqldb.appdomain.cloud"
    end_point = '{0}/{1}'.format(url, location + "_database" + "/_all_docs")
    params = {'include_docs': 'true'}
    response = client.r_session.get(end_point, params=params)
    return response.json()["rows"][index]["doc"][key]
print(getTweetAtIndex(0, "sanfransisco", key = "probability"))

    # TESTED WORKS
def calculateLocationEarthquakeProbability(location):
    client = Cloudant.iam("fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix", "AWLmt1r-iqtEeWTDjEC38l320ufQGsFAheg40iutvxcB")
    client.connect()
    url = "https://fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix:e01ad0f8a3355ea74bf8efeb523cd6da8e8afe94f5a26b2e6af4a7112dd1d144@fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix.cloudantnosqldb.appdomain.cloud"
    end_point = '{0}/{1}'.format(url, location + "_database" + "/_all_docs")
    params = {'include_docs': 'true'}
    response = client.r_session.get(end_point, params=params)
    probabilities = []
    for i in range(10):
       probabilities.append(response.json()["rows"][i]["doc"]["probability"])
    file = open("earthquakeProbability.sav", 'rb')
    earthquakeRegressor = pickle.load(file)
    file.close()
    return earthquakeRegressor.predict([probabilities])

#print(calculateLocationEarthquakeProbability(locations[0])) # expected result


    # TESTED WORKS
# takes the text and probability and insterts it into database
def insertTweet(location, text, probability):
    client = Cloudant.iam("fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix", "AWLmt1r-iqtEeWTDjEC38l320ufQGsFAheg40iutvxcB")
    client.connect()
    jsonDoc= { "tweet": text,
              "probability": probability
            }
    database = databases[location]
    database.create_document(jsonDoc)        
    return
insertTweet("sanfransisco", "i want cheetos", 0.01)

    # TESTED WORKS
# takes in a text and the regression model and calculates the probability of 
# it being due to an earthquake
def calculateRelevance(text, regModel):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='34qzJpNfbmmav0ZFkGM9vM_enLCTAOuQsd5s4odeF19l',
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api')
    
    keywords = {"quake", "shake", "tremble"}
    try:
        response = natural_language_understanding.analyze(
                html=text,
                features=Features(emotion=EmotionOptions())).get_result()
        dictionary = response["emotion"]["document"]["emotion"]
        
    except Exception as e:
        print(e)
        return None
    
    for keyword in keywords:
        columnName = "hasSubstring_" + keyword
        dictionary[columnName] = text.lower().find(keyword) >= 0
        
    one = pd.Series([1])
    data =pd.DataFrame([list(one.append(pd.Series(dictionary)))])
    return regModel.predict(data)