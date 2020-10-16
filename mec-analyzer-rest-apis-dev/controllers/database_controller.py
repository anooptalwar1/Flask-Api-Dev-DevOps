import pymongo
from pymongo import MongoClient
from bson.json_util import dumps

MONGODB_CLIENT_URI = "mongodb://API_URL:27017/"
DATABASE_NAME = "mec_reports_db"
COLLECTION_NAME = "mec_reports_collection"

""" MONGODB Cluster """
cluster = MongoClient(MONGODB_CLIENT_URI)
db = cluster[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def insert_record(record):
    collection.insert_one(record)

def find_all_records():
    cursor = collection.find({}, {'_id': 0})
    return dumps(cursor)

def find_records_by_device_id(deviceId):
    cursor = collection.find({"deviceId": deviceId}, {'_id': 0})
    return dumps(cursor)

def delete_all_records():
    collection.remove({})

