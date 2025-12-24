import os
from pymongo import MongoClient

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")

MongoURI = f"mongodb://{MONGO_HOST}:27017"
DBName = "smart_camera"

client = MongoClient(MongoURI)
mongo_db = client[DBName]

event_logs_collection = mongo_db["event_logs"]