# backend/group.py

from datetime import datetime, timezone
from bson import ObjectId
from backend.db import users_col, groups_col, expenses_col

def list_user_groups(user_id: str) -> list[str]:
    """
    Return a list of group names that the given user_id belongs to.
    """
    oid = ObjectId(user_id)
    cursor = groups_col.find({'members': oid})
    return [g['name'] for g in cursor]


def create_group(name: str, member_usernames: list[str]):
    """
    Create a new group named `name`, with members given by their usernames.
    Raises if any username is not found.
    """
    # look up each user
    member_ids = []
    for uname in member_usernames:
        user = users_col.find_one({'username': uname})
        if not user:
            raise ValueError(f"User '{uname}' not found")
        member_ids.append(user['_id'])

    doc = {
        'name':       name,
        'members':    member_ids,
        'created_at': datetime.now(timezone.utc)
    }
    return groups_col.insert_one(doc)


def add_group_expense(
    group_name: str,
    payer_username: str,
    amount: float,
    category: str,
    date_str: str,
    description: str
):
    """
    Add an expense for the group named `group_name`,
    paid by the user `payer_username`.
    """
    # find the group
    group = groups_col.find_one({'name': group_name})
    if not group:
        raise ValueError(f"Group '{group_name}' not found")

    # find the payer
    payer = users_col.find_one({'username': payer_username})
    if not payer:
        raise ValueError(f"Payer '{payer_username}' not found")

    # parse the date
    try:
        date_obj = datetime.fromisoformat(date_str)
    except Exception:
        raise ValueError(f"Invalid date format: {date_str!r}")

    doc = {
        'user_id':     payer['_id'],
        'group_id':    group['_id'],
        'amount':      float(amount),
        'category':    category,
        'date':        date_obj,
        'description': description
    }
    return expenses_col.insert_one(doc)


def compute_group_balances(group_name: str) -> dict[str, float]:
    """
    For the group named `group_name`, compute each member’s net balance
    (paid minus equal share). Returns a map: username -> balance.
    """
    group = groups_col.find_one({'name': group_name})
    if not group:
        raise ValueError(f"Group '{group_name}' not found")

    members = group['members']

    # sum paid per member_id
    pipeline = [
        {'$match': {'group_id': group['_id']}},
        {'$group': {'_id': '$user_id', 'paid': {'$sum': '$amount'}}}
    ]
    paid_map = {rec['_id']: rec['paid'] for rec in expenses_col.aggregate(pipeline)}

    total = sum(paid_map.values())
    share = total / len(members)

    # map back to username
    balances = {}
    for m_id in members:
        user = users_col.find_one({'_id': m_id})
        uname = user['username'] if user else str(m_id)
        balances[uname] = paid_map.get(m_id, 0) - share

    return balances
