import json
from pathlib import Path
from backend.db import users_col, expenses_col

def load_json(collection, filename):
    path = Path(__file__).parent.parent / "sample_data" / filename
    with open(path, 'r') as f:
        data = json.load(f)
    collection.insert_many(data)
    print(f"Inserted {len(data)} documents into {collection.name}.")

if __name__ == '__main__':
    load_json(users_col, 'dummy_users.json')
    # After inserting users, you can update dummy_expenses.json with actual ObjectIds
    # load_json(expenses_col, 'dummy_expenses.json')