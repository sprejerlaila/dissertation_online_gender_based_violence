#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 10:54:32 2020

@author: lailasprejer
"""

import pandas as pd
import botometer

tweets = pd.read_csv('processed/congress_tweets.csv')
count_users = tweets.screen_name.value_counts().reset_index()
screen_names = count_users[count_users.screen_name > 90]['index'].values
screen_names = ["@" + x for x in screen_names]

rapidapi_key = "XXX" # now it's called rapidapi key
twitter_app_auth = {
    'consumer_key': 'XXXX',
    'consumer_secret': 'XXXX',
    'access_token': 'XXXX',
    'access_token_secret': 'XXXX',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

i = 0
results_list = []
for screen_name, result in bom.check_accounts_in(screen_names):
    i +=1
    results_list.append(result)

screen_name = []
friend = []
network = []
temporal= []
user = []
for res in results_list:
    try:
        screen_name.append(res['user']['screen_name'])
        friend.append(res['categories']['friend'])
        network.append(res['categories']['network'])
        temporal.append(res['categories']['temporal'])
        user.append(res['categories']['user'])
    except:
        continue
    
bots_df = pd.DataFrame({"screen_name":screen_name,"friend":friend,"network":network,"temporal":temporal,"user":user})

def is_bot(x):    
    if x[1] >= 0.8 or x[2] >= 0.8 or x[3] >= 0.8 or x[4] >= 0.8:
        return 1
    return 0

bots_df['is_bot'] = bots_df.apply(is_bot,axis=1)
bots_df.to_csv('bots_df.csv',index=False)



