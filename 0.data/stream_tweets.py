import tweepy
import sys
import json
import time
import pandas as pd

# Load twitter user_id and screen_name information of the politicians
ids = pd.read_csv('twitter_users.csv').id.values
screen_names = pd.read_csv('twitter_users.csv').screen_name.values

auth = tweepy.OAuthHandler()
auth.set_access_token()
api = tweepy.API(auth)

class StreamListener(tweepy.StreamListener):
    def __init__(self, output_file=sys.stdout):
        super(StreamListener,self).__init__()
        self.output_file = output_file
        
    def on_status(self, status):
        with open('tweets{}.json'.format(time.strftime("%y%m%d")), 'a') as tf:
            # Write the json data directly to the file
            json.dump(status._json, tf)
            tf.write('\n')
        
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            return False


stream_listener = StreamListener(output_file='tweets.json')
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)


if __name__ == "__main__":
    while True:
        stream_listener = StreamListener(output_file='tweets{}.json'.format(time.strftime("%y%m%d"))) #Save tweets to daily filss
        stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        try:
            print("streaming...")
            stream.filter(follow=ids, track=screen_names)
        except Exception as e:
            print("error. Restarting Stream... Error:", e)
            time.sleep(60)



