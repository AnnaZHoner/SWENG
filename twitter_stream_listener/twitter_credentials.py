# -*- coding: utf-8 -*-

import json

# create a dictionary to store your twitter credentials

twitter_cred = dict()

# Enter your own consumer_key, consumer_secret, access_key and access_secret
# Replacing the stars ("********")

twitter_cred['CONSUMER_KEY'] = '04FC3oJXzYsJRPuTG4xTXh7rp'
twitter_cred['CONSUMER_SECRET'] = 'fOFp5SRPAXcNtIu6EfzDOulV1ZfWhmjtnb4VaaT8Nml2Q9VSPl'
twitter_cred['ACCESS_KEY'] = '1084208607120580609-Cuck6BaJw35IhDdhT74zdgL8x5dPtM'
twitter_cred['ACCESS_SECRET'] = 'goiceTphkHIAxqbB9o16SRTFL3gDYrphbU9QP5FnxD0Uy'

# Save the information to a json so that it can be reused in code without exposing
# the secret info to public

with open('twitter_credentials.json', 'w') as secret_info:
    json.dump(twitter_cred, secret_info, indent=4, sort_keys=True)
