import bcrypt
from bson import ObjectId
from backend.db import users_col

def register(username, password):
    if users_col.find_one({'username': username}):
        return False, 'Username exists'
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users_col.insert_one({
        'username': username,
        'password_hash': hashed,
        'created_at': None
    })
    return True, 'Registered successfully'

def login(username, password):
    user = users_col.find_one({'username': username})
    if not user:
        return False, 'Invalid credentials'
    if not bcrypt.checkpw(password.encode(), user['password_hash']):
        return False, 'Invalid credentials'
    return True, str(user['_id'])