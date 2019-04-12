
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions
import pandas as pd





    # takes in a twitter text in the form of a string and 
    # creates a row with information such as if it contains the keyword
    # 'quake' and columns on sadness, joy, fear, disgust, and, anger
def constructRow(text, isEarthquake):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='34qzJpNfbmmav0ZFkGM9vM_enLCTAOuQsd5s4odeF19l',
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api'
)
    keywords = {"quake", "shake", "tremble"}
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
        
    print(dictionary)    
    dictionary["duringEarthquake"] = isEarthquake    
    print(pd.Series(dictionary))
    return pd.Series(dictionary)

constructRow("Wakey shakey", isEarthquake= True)

# Dataset with good number of earthquake tweets
tweets = pd.read_json("SF_2014-08-24.json")
earthquakeTweets = tweets.iloc[12000:13306]     # The beginning of the earthquake(earthquake only tweets)
nonEarthquake = tweets.iloc[13307:15000]        # Before the earthquake(non earthquake tweets)

    
dataframe = pd.DataFrame()
i = 0
for index, row in earthquakeTweets.iterrows():
    dataframe = dataframe.append(constructRow(row["text"], True), ignore_index = True)    # isEarthquake column = True
    
for index, row in nonEarthquake.iterrows():
    dataframe = dataframe.append(constructRow(row["text"], False), ignore_index = True)   # isEarthquake column = False

# remove invalid rows that has 0's in the option columns
for index, row in dataframe.iterrows():
    if (row["anger"] == 0 and row["disgust"] == 0 and row["fear"] == 0 and row["joy"] == 0 and row["sadness"] == 0):
        dataframe = dataframe.drop(index)

#-------------------------------------------------------------------------------------------        
        
import numpy as np
# pretend that 'duringEarthquake' variable is our dependant vraibles
Y = dataframe.iloc[:, 2:3].values
# the rest are independant variables
X = dataframe.drop(labels = "duringEarthquake", axis=1)

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2)
# Multiple liner regression
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
# Backward elimination
import statsmodels.formula.api as sm
# adding a constant to the multiple linear regression(need to do so for .OLS())
X = np.append(arr = np.ones((2607, 1)).astype(int), values = X, axis = 1 )



# determining variables of lowest impact
X_opt = X[:, [0,1,2,3,4,5,6,7,8,9]]
regressor_OLS = sm.OLS(endog = Y, exog = X_opt).fit()
regressor_OLS.summary()
# Seems like keyword "earth" was not adding any value to the reggression.
X_opt = X[:, [0,1,2,3,5,6,7,8,9]]
regressor_OLS = sm.OLS(endog = Y, exog = X_opt).fit()
regressor_OLS.summary()

# Need to swap it here
tempdf = pd.DataFrame(X_opt)
columns = tempdf.columns.tolist()
print(columns)
tempdf = tempdf[[0,8,7,3,2,1,6,4,5]]


X_train, X_test, y_train, y_test = train_test_split(tempdf, Y, test_size = 0.2)
regressor = LinearRegression()



regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)


# saving model to file
import pickle
modelFileName = "textRecognitionModel.sav"
file = open(modelFileName, 'wb', pickle.HIGHEST_PROTOCOL)
pickle.dump(regressor, file)
file.close()

file = open("textRecognitionModel.sav", 'rb')
regressor = pickle.load(file)
file.close()

# Preparing data for next training
y_pred = regressor.predict(X_opt)
d = np.append(y_pred, Y, axis =1 )

# Live version will look at the last 10 tweets and determine whether an
# earthquake is happening depending onb those 10 tweets.
# It will only look at the value the the first model gives out

# Need to divide the data set so that each row is 10 consecutive tweet 
# values(will be X(independant variables)) and the corresponding Y(dependant) 
# will be wether if there is an earthquake happening.

row = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
dataset = pd.DataFrame()
NTweets = 10;
for i in range(np.size(d[:,0:1]) - NTweets):
    row = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    for j in range(0 , NTweets):
        row[j] = d[j + i][0] 
        print(d[j + i][0])
    
    row = pd.Series(row)
    dataset= dataset.append(row,  ignore_index=True)
    print("-----------------------------------------")
    

Xreg2 = dataset
Yreg2 = d[0:2597,[1]]



X_train2, X_test2, y_train2, y_test2 = train_test_split(Xreg2,Yreg2, test_size = 0.2)
regressor2 = LinearRegression()
regressor2.fit(X_train2, y_train2)
y_pred2 = regressor2.predict(X_test2)


# saving model to file
import pickle
modelFileName = "earthquakeProbability.sav"
file = open(modelFileName, 'wb')
pickle.dump(regressor2, file,  pickle.HIGHEST_PROTOCOL)
file.close()



file = open(modelFileName, 'rb')
regressor2 = pickle.load(file)
file.close()

y_pred2 = regressor2.predict(X_test2)


# 1st model expectsan input of a tweet

import pickle
file = open("textRecognitionModel.sav", 'rb')
regressor = pickle.load(file)
file.close()

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions
def calculateRelevance(text, regModel):
    
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='34qzJpNfbmmav0ZFkGM9vM_enLCTAOuQsd5s4odeF19l',
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api'
    )
    
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

print(calculateRelevance("I'm so angry, earthquake!", regressor))
# Output result to table with text


from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

client = Cloudant.iam("fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix", "AWLmt1r-iqtEeWTDjEC38l320ufQGsFAheg40iutvxcB")
client.connect()


databaseName = "sanfransisco_tweets"

myDatabase = client.create_database(databaseName)
if myDatabase.exists():
   print ("'{0}' successfully created.\n".format(databaseName))
else:
    print("not exist")





# takes the text and probability and insterts it into the table
def insertTweet(database, text, probability):
    jsonDoc= { "tweet": text,
              "probability": probability
            }
    
    newDocument = database.create_document(jsonDoc)
    if newDocument.exists():
        print("exists")
        
    return

insertTweet(myDatabase, "opa", 0.4)

result_collection = Result(myDatabase.all_docs)
print ("Retrieved minimal document:\n{0}\n".format(result_collection[0]))

result_collection = Result(myDatabase.all_docs, include_docs=True)
print ("Retrieved minimal document:\n{0}\n".format(result_collection[0]))


url = "https://fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix:e01ad0f8a3355ea74bf8efeb523cd6da8e8afe94f5a26b2e6af4a7112dd1d144@fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix.cloudantnosqldb.appdomain.cloud"
end_point = '{0}/{1}'.format(url, databaseName + "/_all_docs")
params = {'include_docs': 'true'}

response = client.r_session.get(end_point, params=params)
print ("{0}\n".format(response.json()))








