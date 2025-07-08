import redis
import os
import json



from dotenv import load_dotenv
load_dotenv()


#region Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
print(REDIS_URL)
redis_client = redis.from_url(REDIS_URL)

def set_cache(key: str, value: dict, ex: int = 3600):
    redis_client.setex(key, ex, json.dumps(value))

def get_cache(key: str) -> dict | None:
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

#endregion


#region Mongo
import pymongo

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "financial_data_cache")

mongo_client = pymongo.MongoClient(MONGO_URL)
mongo_db = mongo_client[MONGO_DB_NAME]
mongo_collection = mongo_db["cache"]

def set_mongo_cache(key: str, value: dict):
    mongo_collection.update_one({"_id": key}, {"$set": value}, upsert=True)

def get_mongo_cache(key: str) -> dict | None:
    doc = mongo_collection.find_one({"_id": key})
    if doc:
        doc.pop("_id")  # Remove the _id field added by MongoDB
        return doc
    return None
#endregion