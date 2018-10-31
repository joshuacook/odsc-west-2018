import pandas as pd
from lib.database import query_database, query_to_dataframe
from pymongo import MongoClient
from bson.binary import Binary
import pickle

if __name__ == "__main__":
    mongo_client = MongoClient('this_mongo')
    data_collection = mongo_client.data.datasets
    
    adult_for_modeling_df = query_to_dataframe("SELECT * FROM adult_for_modeling")
    adult_for_modeling_encoded_df = pd.get_dummies(adult_for_modeling_df)
    features = adult_for_modeling_encoded_df.drop("income_label", axis=1)
    target = adult_for_modeling_encoded_df.income_label

    features_dict = {
        "dataset" : "features",
        "data" : pickle.dumps(features)
    }

    target_dict = {
        "dataset" : "target",
        "data" : pickle.dumps(target)
    }

    data_collection.insert_many([
        features_dict,
        target_dict
    ])
