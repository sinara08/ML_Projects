import pymongo
import pandas as pd
import json

client = pymongo.MongoClient("mongodb+srv://sinara:rootroot@sincluster.0lcik.mongodb.net/?retryWrites=true&w=majority")

DATABASE_NAME='aps'
COLLECTION_NAME = 'sensor'
DATA_FILE_PATH = '/Users/nikhilgopalakrishnan/PycharmProjects/sensor-fault-detection/aps_failure_training_set1.csv'


if __name__ == '__main__':
    df = pd.read_csv(DATA_FILE_PATH)
    print(f'Rows and Columns : {df.shape}')

    #Convert df to json so that we can dump to Mongodb
    df.reset_index(drop=True,inplace=True)
    json_record = list(json.loads(df.T.to_json()).values())
    #print(json_record[0])

    #insert converted json record to Mongo DB
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)

