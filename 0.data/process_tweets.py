import pandas as pd
import json
import pickle
import re
import time

meta_dict_congress = pickle.load(open("meta_dict_congress.pkl", "rb"))

def tidy_tweets(results):
    id_list = []
    screen_name_list, screen_name_gender_list, screen_name_interbloque_list, screen_name_type_list = [], [], [], []

    text_list = []
    in_reply_to_user_id, in_reply_to_status_id, in_reply_to_screen_name = [], [], []
    
    rt_from_screen_name = []
    
    mentions_list, mentions_politicians_list = [], []

    directed_at_screen_name, directed_at_congress, directed_at_gender = [], [], []
    directed_at_state, directed_at_interbloque = [], []

    datetime = []
    location = []

    for idx, tweet in enumerate(results):       
        tweet = json.loads(tweet)
        id_list.append("id_" + str(tweet['id']) if tweet['id'] is not None else None)
        
        screen_name = tweet["user"]['screen_name']
        screen_name_list.append(screen_name)
        screen_name_gender_list.append(meta_dict_congress[screen_name]['gender'] if screen_name in meta_dict_congress else None)
        screen_name_interbloque_list.append(meta_dict_congress[screen_name]['interbloque'] if screen_name in meta_dict_congress else None)
        screen_name_type_list.append(meta_dict_congress[screen_name]['type'] if screen_name in meta_dict_congress else None)

        rp_user_id = tweet["in_reply_to_user_id"]
        rp_screen_name = tweet["in_reply_to_screen_name"]
        rp_status = "id_" + str(tweet["in_reply_to_status_id"]) if tweet["in_reply_to_status_id"] is not None else None

        t = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        datetime.append(t)
        location.append(tweet['place'])
        
        text = tweet['text']
        
        rt_screen_name = None
        dir_screen_name, dir_congress, dir_gender = None, None, None
        dir_state, dir_interbloque = None, None
        
        mentions = set([x['screen_name'] for x in tweet['entities']['user_mentions']])
        
        if 'retweeted_status' in tweet: # It is a retweet 
            text = tweet['retweeted_status']['text']
            try:
                text = tweet['retweeted_status']['extended_tweet']['full_text']
                mentions = set([x['screen_name'] for x in tweet['retweeted_status']['extended_tweet']['entities']['user_mentions']])
            except:
                pass
            rt_screen_name = tweet['retweeted_status']['user']['screen_name']

        if 'quoted_status' in tweet: # In reply to tweet data
            rp_user_id = tweet["quoted_status"]["user"]["id"]
            rp_screen_name = tweet["quoted_status"]["user"]["screen_name"]
            rp_status = "id_" + str(tweet["quoted_status"]["id"])
            
        if 'extended_tweet' in tweet:
            text = tweet['extended_tweet']['full_text']
            mentions = set([x['screen_name'] for x in tweet['extended_tweet']['entities']['user_mentions']])
        
        text = re.sub(r"(?:\@|https?\://)\S+", "", text) # Replacing mentions and urls
        text_list.append(text)
        in_reply_to_status_id.append(rp_status if rp_status else None)
        in_reply_to_user_id.append(rp_user_id)
        in_reply_to_screen_name.append(rp_screen_name)
        rt_from_screen_name.append(rt_screen_name)
        
        if rp_screen_name in meta_dict_congress:            
            dir_screen_name = rp_screen_name
        
        mentions_list.append(mentions)
        mentions_politicians = mentions.intersection(meta_dict_congress.keys())
        
        if rt_screen_name:
            # Remove retweets or replies from mentions. 
            mentions_politicians -= set([rt_screen_name]).union(set([rp_screen_name]))
        
        mentions_politicians_list.append(mentions_politicians)

        if len(mentions_politicians) == 1: # Assume directed tweet
            politician = list(mentions_politicians)[0]
            if rp_screen_name not in meta_dict_congress:
                dir_screen_name = politician
        
        if dir_screen_name:
            dir_congress = meta_dict_congress[dir_screen_name]['type']          
            dir_gender = meta_dict_congress[dir_screen_name]['gender']
            dir_state = meta_dict_congress[dir_screen_name]['state']
            dir_interbloque = meta_dict_congress[dir_screen_name]['interbloque']
                
        directed_at_screen_name.append(dir_screen_name)
        directed_at_congress.append(dir_congress)
        directed_at_gender.append(dir_gender)
        directed_at_state.append(dir_state)
        directed_at_interbloque.append(dir_interbloque)
        
    data = pd.DataFrame({
        "id": id_list,
        "screen_name": screen_name_list,
        "screen_name_type": screen_name_type_list,
        "screen_name_gender": screen_name_gender_list,
        "screen_name_interbloque": screen_name_interbloque_list,
        "directed_at_screen_name":directed_at_screen_name,
        "directed_at_congress":directed_at_congress,
        "directed_at_gender":directed_at_gender,
        "directed_at_state": directed_at_state,
        "directed_at_interbloque": directed_at_interbloque,
        "text": text_list,
        "rt_from_screen_name": rt_from_screen_name,
        "in_reply_to_screen_name": in_reply_to_screen_name,
        "in_reply_to_status_id": in_reply_to_status_id,
        "mentions": mentions_list,
        "mentions_politicians": mentions_politicians_list,
        "datetime":datetime})
    return data