# Format is..
# twitterscraper "near:""San Fransisco, CA"" within:100mi" -bd 2007-10-30 -ed 2007-10-31 -o sf.json -l 1000
# To generate a .bat file to run and collect tweets from the dates that were
# preprocessed in earthquakeDataPreprocessing.py.

import pandas as pd
import datetime

# Need to convert the dates from the dataset format into the twitter 
# compatible format.

# From "mm/dd/yyyy" to "yyyy-mm-dd" 
def convertDate(date):
    newDate = date[6:] + "-" + date[0:2] +  "-" + date[3:5]
    return newDate

# twitterscraper doesn't allow to collect data from a single day so the following
# method is required.    
# Takes in "yyyy-mm-dd" and returns the next day in "yyyy-mm-dd" 
def nextDay(dateString):
    dateToIncrease = datetime.datetime(int(dateString[0:4]), int(dateString[5:7]), int(dateString[8:]))
    dateToIncrease = dateToIncrease + datetime.timedelta(days = 1)
    return (str(dateToIncrease.year) + "-" + str(dateToIncrease.month) + "-" + str(dateToIncrease.day))
    
# Open file made with earthquakeDataPreprocessing.py
dateAndTimes = pd.read_csv("dataAroundSF.csv")
# The specific location string that twitter can accept..
location = "San Fransisco, CA"
maxTweets = "10000"

commands = ""

# Generate commandline commands to extract tweets from a certain date for each date.
for index, row in dateAndTimes.iterrows():
    commands = commands + 'twitterscraper "near:""' + location + '"" within:100mi" -bd ' + convertDate(row['Date']) + ' -ed ' + nextDay(convertDate(row['Date'])) + ' -o ' + "SF_" + convertDate(row['Date']) + '.json -l '+ maxTweets +'\n' 
    
file = open("twitter.bat","w") 
file.write(commands)
file.close()