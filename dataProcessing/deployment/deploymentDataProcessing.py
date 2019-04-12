from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

import pickle
import time


    # Tested Works
def getRawDoc(index):
    client = Cloudant.iam("fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix", "AWLmt1r-iqtEeWTDjEC38l320ufQGsFAheg40iutvxcB")
    client.connect()
    url = "https://fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix:e01ad0f8a3355ea74bf8efeb523cd6da8e8afe94f5a26b2e6af4a7112dd1d144@fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix.cloudantnosqldb.appdomain.cloud"
    end_point = '{0}/{1}'.format(url, "raw_tweets" + "/_all_docs")
    params = {'include_docs': 'true'}
    response = client.r_session.get(end_point, params=params)
    return response.json()["rows"][index]["doc"]



    # Tested Works
# Other option is "_id"
def getRawData(index, key = "tweet"):
    client = Cloudant.iam("fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix", "AWLmt1r-iqtEeWTDjEC38l320ufQGsFAheg40iutvxcB")
    client.connect()
    url = "https://fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix:e01ad0f8a3355ea74bf8efeb523cd6da8e8afe94f5a26b2e6af4a7112dd1d144@fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix.cloudantnosqldb.appdomain.cloud"
    end_point = '{0}/{1}'.format(url, "raw_tweets" + "/_all_docs")
    params = {'include_docs': 'true'}
    response = client.r_session.get(end_point, params=params)
    print(response.json()["rows"][index]["doc"])
    return response.json()["rows"][index]["doc"][key]


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
#print(getTweetAtIndex(0, "sanfransisco", key = "probability"))

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
def insertTweet(database, text, probability):
    client = Cloudant.iam("fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix", "AWLmt1r-iqtEeWTDjEC38l320ufQGsFAheg40iutvxcB")
    client.connect()
    jsonDoc= { "tweet": text,
              "probability": probability
            }
    database.create_document(jsonDoc)        
    return
#insertTweet("sanfransisco", "i want cheetos", 0.01)

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


client = Cloudant.iam("fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix", "AWLmt1r-iqtEeWTDjEC38l320ufQGsFAheg40iutvxcB")
client.connect()
alert_database = client.create_database("alert_database")

databases= {}
locations = []

    #begin parsing tweets
# regressor for calculateRelveance()
file = open("textRecognitionModel.sav", 'rb')
relevanceRegressor = pickle.load(file)
file.close()

lastIdRead =  getRawDoc(0)
lastIdRead = lastIdRead['id']

while True:
    doc = getRawDoc(0)
    print(doc)
    idTmp = doc["id"]
    i = 0 #if idTmp somehow missed lastIdRead    
    if lastIdRead != idTmp:
        lastIdRead = idTmp
    while (lastIdRead != idTmp and i < 10):
        location = doc["location"]
        location = location.lower()
        location = location.replace(" ", "_")
        if (location not in locations):
            client = Cloudant.iam("fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix", "AWLmt1r-iqtEeWTDjEC38l320ufQGsFAheg40iutvxcB")
            client.connect()
            databases[location] = client.create_database(location + "_database")
            locations.append(location)
            
        text = doc["text"]
        probability = calculateRelevance(text, relevanceRegressor)
        insertTweet(databases[location], text, probability)
        i = i + 1  
        getRawDoc(i)
    i = 0
    
    for location in locations:
        probability = calculateLocationEarthquakeProbability(location)
        jsonDoc= { "location": location,
              "probability": probability
            }
        alert_database.create_document(jsonDoc)   
    
    time.sleep(1)
        
        
