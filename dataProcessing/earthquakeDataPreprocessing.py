import pandas as pd
from math import cos


# Idea is to (manually?) select a city with a high earthquake occurance 
# and then calculate the range from kilometers to longitude and latitude 
# of which we extract earthquake occurances from within the range in the 
# dataset.

dataset = pd.read_csv('database.csv')

# Can't extract tweets before around 2007 so cutting off all dates before 2007
# Tweets before 2010 werent able to be scraped so now cutting off all tweets before 2010
indexOfDate = 20397
relevantDates = dataset.iloc[17826:-1, :]

#   Choosing Sanfransisco as the city
#   San Fransisco co - ordinates : 37.737708, -122.426607
#   Formulae for converting km into co-ordinates
#   Latitude: 1 deg = 110.574 km
#   Longitude: 1 deg = 111.320*cos(latitude) km
SFLatitude = 37.737708
SFLongitude = -122.426607
KmRange = 600

# Calculating the range to consider 
minLatitude = SFLatitude - (KmRange/110.574)
maxLatitude = SFLatitude + (KmRange/110.574)
minLongitude = SFLongitude - (KmRange / (111.320 * cos(minLatitude)))
maxLongitude = SFLongitude + (KmRange / (111.320 * cos(maxLatitude)))
minMagnitude = 6.0

# Getting indices which have out of range co-ordinates
indexMinLat = relevantDates[relevantDates['Latitude'] < minLatitude  ].index
indexMaxLat = relevantDates[relevantDates['Latitude'] > maxLatitude  ].index
indexMinLong = relevantDates[relevantDates['Longitude'] < minLongitude ].index
indexMaxLong = relevantDates[relevantDates['Longitude'] > maxLongitude ].index
indexMagnitude = relevantDates[relevantDates['Magnitude'] < minMagnitude].index

# Union the indices together
indicesToGetRidOf = list(set(indexMagnitude)|set(indexMinLat) | set(indexMaxLat) | set(indexMinLong) | set(indexMaxLong))

# Getting rid of the indices that are out of range
relevantDates.drop(indicesToGetRidOf, inplace=True)

# Getting rid of the extra columns('Type' onwards..)
relevantDates = relevantDates.iloc[:, 0: 4 ]
    
# Export data to csv
relevantDates.to_csv(r'dataAroundSF.csv')
    

