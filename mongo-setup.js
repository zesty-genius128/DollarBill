// mongo-setup.js
// ------------------
// Switch to your database
//use dollar_bill;

// 1. Define JSON-Schema validators for each collection

const userSchema = {
  $jsonSchema: {
    bsonType: "object",
    required: ["username", "password_hash", "created_at"],
    properties: {
      username:      { bsonType: "string" },
      password_hash: { bsonType: "string" },
      created_at:    { bsonType: "date" }
    }
  }
};

const expenseSchema = {
  $jsonSchema: {
    bsonType: "object",
    required: ["user_id", "amount", "category", "date", "description"],
    properties: {
      user_id:    { bsonType: "objectId" },
      amount:     { bsonType: ["double","int","decimal"] },
      category:   { bsonType: "string" },
      date:       { bsonType: "date" },
      description:{ bsonType: "string" },
      group_id:   { bsonType: ["objectId","null"] },
      payer_id:   { bsonType: ["objectId","null"] }
    }
  }
};

const groupSchema = {
  $jsonSchema: {
    bsonType: "object",
    required: ["name","members","created_at"],
    properties: {
      name:       { bsonType: "string" },
      members:    {
        bsonType: "array",
        items:    { bsonType: "objectId" }
      },
      created_at: { bsonType: "date" }
    }
  }
};

// Helper to create or modify a collection with validator
function upsertColl(name, schema) {
  const exists = db.getCollectionInfos({ name }).length > 0;
  if (!exists) {
    print(`Creating '${name}' with validator…`);
    db.createCollection(name, { validator: schema });
  } else {
    print(`Updating validator for '${name}'…`);
    db.runCommand({
      collMod: name,
      validator: schema,
      validationLevel: "moderate"
    });
  }
}

upsertColl("users",    userSchema);
upsertColl("expenses", expenseSchema);
upsertColl("groups",   groupSchema);

// 2. Create indexes for performance

print("Creating indexes…");
db.users.createIndex({ username: 1 }, { unique: true });

db.expenses.createIndex({ user_id: 1 });
db.expenses.createIndex({ date: 1 });
db.expenses.createIndex({ category: 1 });
db.expenses.createIndex({ group_id: 1 });

db.groups.createIndex({ name: 1 }, { unique: true });
db.groups.createIndex({ members: 1 });

// 3. Back-fill new fields on existing expense docs

print("Adding default fields to existing expenses…");
db.expenses.updateMany(
  {}, 
  { $set: { group_id: null, payer_id: null } }
);

// 4. (Optional) Seed a sample group called “Roommates”

// Make sure users “arjun” and “aditya” exist first
const u1 = db.users.findOne({ username: "arjun"   });
const u2 = db.users.findOne({ username: "aditya"  });
if (u1 && u2) {
  print("Upserting sample group 'Roommates'…");
  db.groups.updateOne(
    { name: "Roommates" },
    { 
      $setOnInsert: { 
        name:       "Roommates", 
        members:    [u1._id, u2._id], 
        created_at: new Date() 
      }
    },
    { upsert: true }
  );
} else {
  print("One or both sample users not found—skipping sample group.");
}

print("✅ MongoDB setup complete!");
