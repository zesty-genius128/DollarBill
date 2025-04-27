from bson import ObjectId
from backend.db import expenses_col

def add_expense(user_id, amount, category, date, description, group_id=None):
    doc = {
        'user_id': ObjectId(user_id),
        'amount': amount,
        'category': category,
        'date': date,
        'description': description,
        'group_id': ObjectId(group_id) if group_id else None
    }
    return expenses_col.insert_one(doc)

def update_expense(expense_id, user_id, **fields):
    return expenses_col.update_one(
        {'_id': ObjectId(expense_id), 'user_id': ObjectId(user_id)},
        {'$set': fields}
    )

def delete_expense(expense_id, user_id):
    return expenses_col.delete_one({
        '_id': ObjectId(expense_id),
        'user_id': ObjectId(user_id)
    })

def fetch_expenses(user_id, filters=None):
    query = {'user_id': ObjectId(user_id)}
    if filters:
        query.update(filters)
    return list(expenses_col.find(query))