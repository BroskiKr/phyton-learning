from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27018/")

db = client["usersDB"]

users_collection = db["users"]
