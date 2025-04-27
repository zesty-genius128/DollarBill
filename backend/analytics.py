from bson import ObjectId
from backend.db import expenses_col

def monthly_summary(user_id):
    pipeline = [
        {'$match': {'user_id': ObjectId(user_id)}},
        {'$group': {
            '_id': {'year': {'$year': '$date'}, 'month': {'$month': '$date'}},
            'total': {'$sum': '$amount'}
        }},
        {'$sort': {'_id.year': 1, '_id.month': 1}}
    ]
    return list(expenses_col.aggregate(pipeline))

# Similar functions for yearly_summary, category_trend, etc.