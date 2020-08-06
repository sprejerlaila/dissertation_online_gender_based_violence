#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 10:19:23 2020

@author: lailasprejer
"""
import pandas as pd
import requests
from requests_oauthlib import OAuth1
meta = pd.read_csv('metadata.csv')
oauth = OAuth1("XXXXXXX",
               "XXXXXXX",
               "XXXXXXX",
               "XXXXXXX")

followers_count = []
friends_count = []
statuses_count = []
favourites_count = []

for screen_name in meta.screen_name.values:
    url = "https://api.twitter.com/1.1/users/show.json?" + \
        "screen_name={}".format(screen_name) + "&include_entities=true"
    response = requests.get(url, auth=oauth)
    try:
        followers_count.append(response.json()['followers_count'])
        friends_count.append(response.json()['friends_count'])
        statuses_count.append(response.json()['statuses_count'])
        favourites_count.append(response.json()['favourites_count'])
    except:
        followers_count.append("")
        friends_count.append("")
        statuses_count.append("")
        favourites_count.append("")
        print(screen_name)
        
meta['followers_count'] = followers_count
meta['friends_count'] = friends_count
meta['statuses_count'] = statuses_count
meta['favourites_count'] = favourites_count