from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://adamerla128:Purdue@5139@dollarbill.htzwrxa.mongodb.net/dollarbill?retryWrites=true&w=majority")

client = MongoClient(MONGO_URI)
db = client["dollar_bill"]

users_col = db["users"]
expenses_col = db["expenses"]
groups_col = db["groups"]
