import json
from cloudant.client import Cloudant

with open('test_cloudant.json') as cred:
    cred = json.load(cred)
    username = cred['username']
    password = cred['password']
    url = cred['url']
    account_name = username

client = Cloudant(username, password, url=url, account=account_name, connect=True)

session = client.session()

my_database = client.create_database('raw_tweets')
#creating a database
#my_database = client.create_database('my_database')

#if my_database.exists():
    #print('SUCCESS!')
#my_database = client['my_database']
#creating document content area
#data = {'name': 'aa','age': 20}
#create document
#doc = my_database.create_document(data)

# Disconnect from the server
client.disconnect()
