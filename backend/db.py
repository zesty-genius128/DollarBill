from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['dollar_bill']

users_col = db['users']
expenses_col = db['expenses']
groups_col = db['groups']