# backend/expenses.py

from datetime import datetime
from bson import ObjectId
from backend.db import expenses_col

def add_expense(user_id: str,
                amount: float,
                category: str,
                date_str: str,
                description: str,
                group_id: str = None,
                payer_id: str = None):
    """
    Insert a new expense document, converting date_str (ISO) into a datetime.
    """
    try:
        date_obj = datetime.fromisoformat(date_str)
    except Exception:
        raise ValueError(f"Invalid date format: {date_str!r}")

    doc = {
        'user_id':     ObjectId(user_id),
        'amount':      float(amount),
        'category':    category,
        'date':        date_obj,
        'description': description,
        'group_id':    ObjectId(group_id) if group_id else None,
        'payer_id':    ObjectId(payer_id) if payer_id else None
    }
    return expenses_col.insert_one(doc)

def update_expense(expense_id: str,
                   user_id: str,
                   amount: float = None,
                   category: str = None,
                   date_str: str = None,
                   description: str = None):
    """
    Update an existing expense. Only provided fields will be changed.
    """
    updates = {}
    if amount is not None:
        updates['amount'] = float(amount)
    if category is not None:
        updates['category'] = category
    if date_str is not None:
        try:
            updates['date'] = datetime.fromisoformat(date_str)
        except Exception:
            raise ValueError(f"Invalid date format: {date_str!r}")
    if description is not None:
        updates['description'] = description

    if not updates:
        return None  # nothing to update

    return expenses_col.update_one(
        {'_id': ObjectId(expense_id), 'user_id': ObjectId(user_id)},
        {'$set': updates}
    )

def delete_expense(expense_id: str, user_id: str):
    """
    Delete an expense by its ID, ensuring it belongs to the given user.
    """
    return expenses_col.delete_one({
        '_id': ObjectId(expense_id),
        'user_id': ObjectId(user_id)
    })

def list_expenses(user_id: str,
                  start_date: str = None,
                  end_date: str = None,
                  category: str = None):
    """
    Fetch expenses for a user, optionally filtered by date range or category.
    Returns a list of dicts.
    """
    query = {'user_id': ObjectId(user_id)}
    if category:
        query['category'] = category
    if start_date:
        try:
            query.setdefault('date', {})['$gte'] = datetime.fromisoformat(start_date)
        except Exception:
            raise ValueError(f"Invalid start_date: {start_date!r}")
    if end_date:
        try:
            query.setdefault('date', {})['$lte'] = datetime.fromisoformat(end_date)
        except Exception:
            raise ValueError(f"Invalid end_date: {end_date!r}")

    cursor = expenses_col.find(query).sort('date', -1)
    return list(cursor)

# ---- ALIAS FOR FRONTEND ----
# The UI expects fetch_expenses(), so we alias it here:
fetch_expenses = list_expenses
