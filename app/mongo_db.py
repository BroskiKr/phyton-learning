from pymongo import MongoClient
from app import settings

client = MongoClient(settings.MONGODB_URL)

db = client["usersDB"]

users_collection = db["users"]
