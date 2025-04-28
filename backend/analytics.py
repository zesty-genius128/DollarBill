from bson import ObjectId
from backend.db import expenses_col

def monthly_summary(user_id):
    pipeline = [
        {'$match': {'user_id': ObjectId(user_id)}},
        {'$group': {
            '_id': {'year': {'$year': {'$toDate': '$date'}},
                    'month': {'$month': {'$toDate': '$date'}}},
            'total': {'$sum': '$amount'}
        }},
        {'$sort': {'_id.year': 1, '_id.month': 1}}
    ]
    return list(expenses_col.aggregate(pipeline))

def yearly_summary(user_id):
    pipeline = [
        {'$match': {'user_id': ObjectId(user_id)}},
        {'$group': {
            '_id': {'year': {'$year': {'$toDate': '$date'}}},
            'total': {'$sum': '$amount'}
        }},
        {'$sort': {'_id.year': 1}}
    ]
    return list(expenses_col.aggregate(pipeline))

def category_trend(user_id):
    pipeline = [
        {'$match': {'user_id': ObjectId(user_id)}},
        {'$group': {
            '_id': {'category': '$category'},
            'total': {'$sum': '$amount'}
        }},
        {'$sort': {'total': -1}}
    ]
    return list(expenses_col.aggregate(pipeline))