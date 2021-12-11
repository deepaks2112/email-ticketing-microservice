import pymongo
from pymongo import MongoClient, IndexModel
from tools.config import config, Constants


mongo = MongoClient(config.MONGO_URL)
mongo_db = mongo[config.DB_NAME]

ticket_id_index = ("ticket_id", pymongo.ASCENDING)
user_created_at_index = [("ticket_details.user", pymongo.ASCENDING), ("created_at", pymongo.DESCENDING)]

mongo_db[Constants.TICKET_RECORD_COLLECTION].create_index([ticket_id_index], unique=True)
mongo_db[Constants.TICKET_RECORD_COLLECTION].create_index([*user_created_at_index])
