# backend/db.py
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

load_dotenv()

USER     = quote_plus(os.getenv("MONGO_USER"))
PASSWORD = quote_plus(os.getenv("MONGO_PASS"))
HOST     = os.getenv("MONGO_HOST")
DBNAME   = os.getenv("MONGO_DBNAME", "dollar_bill")

MONGO_URI = (
    f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DBNAME}"
    "?retryWrites=true&w=majority"
)

# tell PyMongo to use certifi’s CA bundle
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
db     = client[DBNAME]

users_col    = db["users"]
expenses_col = db["expenses"]
groups_col   = db["groups"]
