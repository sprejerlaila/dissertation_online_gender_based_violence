import pandas as pd
import process_tweets
import os

files = os.listdir('raw')

df_list = []

for idx, file in enumerate(files): 
    print("Processing file N", idx, "from", len(files)-1)
    print(">> Reading tweets")
    with open('/raw/{}'.format(file)) as json_data:
        tweets = json_data.readlines()[1:]
    
    print(">> Tidying tweets")
    df = process_tweets.tidy_tweets(tweets)
    df_list.append(df)
    
    if idx == 30:
        all_files = pd.concat(df_list)
        print(">>> Saving to csv1")
        all_files.to_csv("processed/congress_tweets1.csv", index = False)
        del all_files
        del df_list
        df_list = []
        
    if idx == 60:
        ll_files = pd.concat(df_list)
        print(">>> Saving to csv2")
        all_files.to_csv("processed/congress_tweets2.csv", index = False)
        del all_files
        del df_list
        df_list = []

all_files = pd.concat(df_list)
print(">>> Saving to csv3")
all_files.to_csv("processed/congress_tweets3.csv", index = False)
del all_files

df1 = pd.read_csv("processed/congress_tweets1.csv")
df2 = pd.read_csv("processed/congress_tweets2.csv")
df3 = pd.read_csv("processed/congress_tweets3.csv")
df = pd.concat([df1,df2,df3])

df.drop_duplicates("id").to_csv('processed/congress_tweets.csv',index=False)

