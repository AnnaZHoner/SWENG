class LocationStats(object):
    location = "San Fransisco, CA"
    numberContainigQuake = 0
    numberNotContainingQuake = 0
    tweets = []
    numberOfNewestTweetsToLookAt = 30
    # if there are 3 tweets containing "earthquake" to 1 not containing, it will trigger the alert
    alarmThreshold = 3
    
    # The class "constructor" - It's actually an initializer 
    def __init__(self, numberOfNewestTweetsToLookAt, alarmThreshold):
        self.numberOfNewestTweetsToLookAt = numberOfNewestTweetsToLookAt
        self.alarmThreshold = alarmThreshold

def make_location(numberOfNewestTweetsToLookAt, alarmThreshold):
    locationStats = LocationStats(numberOfNewestTweetsToLookAt, alarmThreshold)
    return locationStats

    def processTweetAndUpdateStats(self, text):
    
    
