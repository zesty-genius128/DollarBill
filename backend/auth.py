# backend/auth.py

import bcrypt
from datetime import datetime, timezone
from backend.db import users_col

def register(username: str, password: str) -> tuple[bool, str]:
    """
    Register a new user.
    Returns (True, user_id) on success, or (False, error_message) if username taken.
    """
    if users_col.find_one({'username': username}):
        return False, 'Username already exists'

    # Hash the password and decode to UTF-8 for storage
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_str = hashed_bytes.decode('utf-8')

    user_doc = {
        'username':      username,
        'password_hash': hashed_str,
        'created_at':    datetime.now(timezone.utc)
    }
    result = users_col.insert_one(user_doc)
    return True, str(result.inserted_id)

def login(username: str, password: str) -> tuple[bool, str]:
    """
    Authenticate a user.
    Returns (True, user_id) on success, or (False, error_message) on failure.
    """
    user = users_col.find_one({'username': username})
    if not user:
        return False, 'Invalid credentials'

    # Re-encode stored hash and check
    stored_hash = user.get('password_hash', '')
    if not bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return False, 'Invalid credentials'

    return True, str(user['_id'])
