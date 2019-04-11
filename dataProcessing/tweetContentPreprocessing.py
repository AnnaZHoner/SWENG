
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EmotionOptions
import pandas as pd


natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='34qzJpNfbmmav0ZFkGM9vM_enLCTAOuQsd5s4odeF19l',
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api'
)

keywords = {"quake", "shake", "tremble"}

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


X_train, X_test, y_train, y_test = train_test_split(X_opt, Y, test_size = 0.2)
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

