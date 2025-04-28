# scripts/seed_data.py

import sys
from pathlib import Path
from datetime import datetime
import json

# ─── Make project root importable ─────────────────────────────────────────────
project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root))
# ──────────────────────────────────────────────────────────────────────────────

from backend.db import users_col, expenses_col, groups_col

def load_users():
    path = project_root / "sample_data" / "dummy_users.json"
    users = json.loads(path.read_text())
    to_insert = []
    for u in users:
        # Convert ISO string to datetime
        dt = datetime.fromisoformat(u["created_at"].replace("Z", "+00:00"))
        to_insert.append({
            "username":      u["username"],
            "password_hash": u["password_hash"],
            "created_at":    dt
        })
    if to_insert:
        users_col.insert_many(to_insert)
        print(f"✅ Inserted {len(to_insert)} users")

def load_expenses():
    path = project_root / "sample_data" / "dummy_expenses.json"
    raw = json.loads(path.read_text())
    to_insert = []
    for e in raw:
        user = users_col.find_one({"username": e["username"]})
        if not user:
            print(f"⚠️ User '{e['username']}' not found; skipping expense")
            continue
        # build the document with proper types
        doc = {
            "user_id":    user["_id"],
            "amount":     e["amount"],
            "category":   e["category"],
            "date":       datetime.fromisoformat(e["date"].replace("Z", "+00:00")),
            "description":e["description"],
            "group_id":   None,
            "payer_id":   None
        }
        to_insert.append(doc)
    if to_insert:
        expenses_col.insert_many(to_insert)
        print(f"✅ Inserted {len(to_insert)} expenses")

def load_groups():
    path = project_root / "sample_data" / "dummy_groups.json"
    raw = json.loads(path.read_text())
    for g in raw:
        # look up member IDs
        members = []
        for username in g["members"]:
            user = users_col.find_one({"username": username})
            if user:
                members.append(user["_id"])
        if not members:
            print(f"⚠️ No valid members for group '{g['name']}', skipping")
            continue
        groups_col.update_one(
            { "name": g["name"] },
            {
                "$setOnInsert": {
                    "name":       g["name"],
                    "members":    members,
                    "created_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        print(f"✅ Upserted group '{g['name']}' with {len(members)} members")

if __name__ == "__main__":
    load_users()
    load_expenses()
    load_groups()
    print("🎉 Seeding complete!")
