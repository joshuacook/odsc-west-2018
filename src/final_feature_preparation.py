import pickle
from pymongo import MongoClient
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

mongo_client = MongoClient('this_mongo')
data_collection = mongo_client.data.datasets

target_dict_from_mongo = data_collection.find_one({"dataset" : "target"})
target_from_mongo = pickle.loads(target_dict_from_mongo["data"])
features_dict_from_mongo = data_collection.find_one({"dataset" : "features"})
features_from_mongo = pickle.loads(features_dict_from_mongo["data"])

rfc = RandomForestClassifier(n_estimators=30)
grid_search = GridSearchCV(rfc, {}, cv=5, return_train_score=False)

grid_search.fit(features_from_mongo, target_from_mongo)
best_estimator = grid_search.best_estimator_
feature_importances = best_estimator.feature_importances_
feature_importances = pd.Series(feature_importances, index=features_from_mongo.columns)
feature_importances = feature_importances.sort_values(ascending=False)

binary_features = list(feature_importances.index)
binary_features.remove("age")
binary_features.remove("hours_per_week")
binary_features.remove("capital_gain")
binary_features.remove("capital_loss")

final_features_names = binary_features[:8]

final_features_names_dict = {
    "dataset" : "final_features_names",
    "data" : final_features_names
}

data_collection.delete_many({
    "dataset" : "final_features_names"
})
data_collection.insert_one(final_features_names_dict)
