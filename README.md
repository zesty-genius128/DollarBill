# 💰 DollarBill

A full-stack expense tracking and group splitting application built with Streamlit and MongoDB. Track your personal expenses, visualize spending patterns, and easily split bills with friends or roommates.

## ✨ Features

- **User Authentication**: Secure registration and login with bcrypt password hashing
- **Personal Expense Tracking**: Add, view, edit, and delete your expenses
- **Rich Analytics**: Visualize your spending with monthly, yearly, and category breakdowns
- **Group Expense Management**: Create groups with friends and split expenses fairly
- **Automated Balance Calculation**: Instantly see who owes what in group expenses
- **Interactive Dashboard**: Beautiful, user-friendly interface built with Streamlit

## 🛠️ Technology Stack

**Frontend:**
- Streamlit - Interactive web UI framework
- Matplotlib - Data visualization

**Backend:**
- Python 3.x
- PyMongo - MongoDB driver
- bcrypt - Password hashing

**Database:**
- MongoDB Atlas (cloud) or local MongoDB instance

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Node.js and npm (for MongoDB setup scripts)
- A MongoDB instance (local or MongoDB Atlas account)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/zesty-genius128/DollarBill.git
cd DollarBill
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies (for MongoDB setup)

```bash
npm install
```

## ⚙️ Configuration

### 1. Set Up Environment Variables

Create a `.env` file in the root directory with your MongoDB credentials:

```env
MONGO_USER=your_mongodb_username
MONGO_PASS=your_mongodb_password
MONGO_HOST=your_mongodb_host
MONGO_DBNAME=dollar_bill
```

**Example for MongoDB Atlas:**
```env
MONGO_USER=myuser
MONGO_PASS=mypassword
MONGO_HOST=cluster0.xxxxx.mongodb.net
MONGO_DBNAME=dollar_bill
```

**Example for Local MongoDB:**
```env
MONGO_USER=admin
MONGO_PASS=admin123
MONGO_HOST=localhost:27017
MONGO_DBNAME=dollar_bill
```

### 2. Initialize the Database

Run the MongoDB setup script to create collections with validation schemas and indexes:

```bash
mongosh "mongodb+srv://your-connection-string" --file mongo-setup.js
```

Or for local MongoDB:
```bash
mongosh "mongodb://localhost:27017/dollar_bill" --file mongo-setup.js
```

### 3. (Optional) Seed Sample Data

Load sample users, expenses, and groups for testing:

```bash
python scripts/seed_data.py
```

This creates two sample users:
- Username: `arjun` / Password: `password`
- Username: `aditya` / Password: `password`

## 🎯 Usage

### Start the Application

```bash
streamlit run frontend/app.py
```

The application will open in your default browser at `http://localhost:8501`.

### First-Time Setup

1. **Register**: Create a new account with a username and password
2. **Login**: Sign in with your credentials
3. **Add Expenses**: Navigate to the "Expenses" tab to start tracking your spending
4. **View Analytics**: Check the "Analytics" tab for visual insights
5. **Create Groups**: Go to "Groups" tab to create expense-splitting groups with friends

### Key Features Guide

#### Personal Expenses
- **Add**: Enter amount, category, date, and description
- **View/Edit**: Browse your expenses and update details as needed
- **Delete**: Remove expenses you no longer need to track

#### Analytics
- **Monthly Summary**: Bar chart showing spending trends by month
- **Yearly Summary**: Overview of annual spending patterns
- **Category Breakdown**: Pie chart of expenses by category

#### Group Management
- **Create Groups**: Enter group name and comma-separated usernames
- **Add Group Expenses**: Record who paid and split among members
- **View Balances**: See who owes what with one click

## 📁 Project Structure

```
DollarBill/
├── backend/                 # Backend logic and database operations
│   ├── __init__.py
│   ├── analytics.py        # Aggregation queries for analytics
│   ├── auth.py             # User registration and login
│   ├── db.py               # MongoDB connection setup
│   ├── expenses.py         # CRUD operations for expenses
│   ├── group.py            # Group management and balance calculation
│   ├── utils.py            # Utility functions
│   └── visuals.py          # Chart generation with matplotlib
├── frontend/
│   └── app.py              # Main Streamlit application
├── sample_data/            # Sample JSON data for testing
│   ├── dummy_users.json
│   ├── dummy_expenses.json
│   └── dummy_groups.json
├── scripts/
│   └── seed_data.py        # Script to load sample data
├── mongo-setup.js          # MongoDB schema and index setup
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies
└── README.md
```

## 🗄️ Database Schema

### Users Collection
```javascript
{
  username: String (unique),
  password_hash: String,
  created_at: Date
}
```

### Expenses Collection
```javascript
{
  user_id: ObjectId,
  amount: Number,
  category: String,
  date: Date,
  description: String,
  group_id: ObjectId (optional),
  payer_id: ObjectId (optional)
}
```

### Groups Collection
```javascript
{
  name: String (unique),
  members: [ObjectId],
  created_at: Date
}
```

## 🔒 Security Notes

- Passwords are hashed using bcrypt before storage
- MongoDB connection uses TLS/SSL for secure communication
- Never commit `.env` file to version control
- Sample users have weak passwords - change them in production!

## 🤝 Contributing

This is a database systems term project. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is created as a term project for educational purposes.

## 👥 Authors

Database Systems Term Project Team

## 🐛 Troubleshooting

**Connection Issues:**
- Verify `.env` credentials are correct
- Check MongoDB server is running (for local instances)
- Ensure IP whitelist includes your IP (for MongoDB Atlas)

**Module Not Found:**
- Run `pip install -r requirements.txt` again
- Verify you're in the correct directory

**Charts Not Displaying:**
- Ensure you have expense data in the database
- Check that matplotlib is properly installed
