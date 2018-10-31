import pickle
from pymongo import MongoClient
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

mongo_client = MongoClient('this_mongo')
data_collection = mongo_client.data.datasets
predictions_collection = mongo_client.data.predictions

target_dict_from_mongo = data_collection.find_one({"dataset" : "target"})
target_from_mongo = pickle.loads(target_dict_from_mongo["data"])
features_dict_from_mongo = data_collection.find_one({"dataset" : "features"})
features_from_mongo = pickle.loads(features_dict_from_mongo["data"])
final_features_names_dict_from_mongo = data_collection.find_one({"dataset" : "final_features_names"})
final_features_names_from_mongo = final_features_names_dict_from_mongo["data"]

rfc = RandomForestClassifier(n_estimators=30)
grid_search = GridSearchCV(rfc, {}, cv=5, return_train_score=False)
grid_search.fit(features_from_mongo[final_features_names_from_mongo], target_from_mongo)
best_estimator = grid_search.best_estimator_

marital_status_Married = [0, 1]
relationship_Husband   = [0, 1]
marital_status_Never   = [0, 1]
education_Bachelors    = [0, 1]
occupation_Exec        = [0, 1]
occupation_Prof        = [0, 1]
gender                 = [0, 1]
education_Masters      = [0, 1]

features_for_lookup = [
    [val_1, val_2, val_3, val_4, val_5, val_6, val_7, val_8]
        for val_1 in marital_status_Married
        for val_2 in relationship_Husband
        for val_3 in marital_status_Never
        for val_4 in education_Bachelors
        for val_5 in occupation_Exec
        for val_6 in occupation_Prof
        for val_7 in gender
        for val_8 in education_Masters
]

features_for_lookup_np = np.array(features_for_lookup)

predictions = best_estimator.predict(features_for_lookup_np)

marital_status_Married = ['0', '1']
relationship_Husband   = ['0', '1']
marital_status_Never   = ['0', '1']
education_Bachelors    = ['0', '1']
occupation_Exec        = ['0', '1']
occupation_Prof        = ['0', '1']
gender                 = ['0', '1']
education_Masters      = ['0', '1']

features_as_keys = [
    ''.join([val_1, val_2, val_3, val_4, val_5, val_6, val_7, val_8])
        for val_1 in marital_status_Married
        for val_2 in relationship_Husband
        for val_3 in marital_status_Never
        for val_4 in education_Bachelors
        for val_5 in occupation_Exec
        for val_6 in occupation_Prof
        for val_7 in gender
        for val_8 in education_Masters
]

lookup_table = [
    {"feature_set" : feature_set,
     "prediction" : prediction }
    for feature_set, prediction in zip(features_as_keys, predictions.astype(str))
]

predictions_collection.drop()

predictions_collection.insert_many(lookup_table)
