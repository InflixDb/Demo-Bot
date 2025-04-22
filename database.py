from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client["temp_filter_bot"]
filters_col = db["filters"]

def add_filter(keyword, message_id):
    filters_col.update_one({"keyword": keyword.lower()}, {"$set": {"message_id": message_id}}, upsert=True)

def get_filter(keyword):
    result = filters_col.find_one({"keyword": keyword.lower()})
    return result["message_id"] if result else None
