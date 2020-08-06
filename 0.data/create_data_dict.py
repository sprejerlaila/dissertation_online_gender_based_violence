
import pandas as pd
import pickle

meta = pd.read_csv("metadata.csv")

meta_dict_congress = {}

for idx, row in meta.iterrows():
    if row['screen_name']:
        meta_dict[row['screen_name']] = {
            "gender" : row['gender'],
            "type" : row['type'],
            "name" : row['name'],
            "lastname" : row['lastname'],
            "state": row['provincia'],
            "party": row['partido'],
            "bloque": row['bloque'],
            "interbloque": row['interbloque']
        }

pickle.dump(meta_dict, open( "meta_dict_congress.pkl", "wb" ) )