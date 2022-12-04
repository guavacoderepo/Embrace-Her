from pymongo import MongoClient
import os

mongo = MongoClient(os.environ.get("MONGO_HOST"))