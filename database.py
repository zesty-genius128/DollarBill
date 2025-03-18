import sqlite3

DATABASE_NAME = 'expenses.db'

def get_connection():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)

def create_tables():
    """Create the necessary tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # Create group_expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_id INTEGER NOT NULL,
            group_name TEXT NOT NULL,
            participants TEXT NOT NULL,
            individual_share REAL,
            FOREIGN KEY(expense_id) REFERENCES expenses(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(amount, category, date, description):
    """Insert a new expense record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (amount, category, date, description)
        VALUES (?, ?, ?, ?)
    ''', (amount, category, date, description))
    conn.commit()
    conn.close()

def update_expense(expense_id, amount=None, category=None, date=None, description=None):
    """Update an existing expense record. Only non-null fields are updated."""
    conn = get_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    if amount is not None:
        fields.append("amount=?")
        values.append(amount)
    if category is not None:
        fields.append("category=?")
        values.append(category)
    if date is not None:
        fields.append("date=?")
        values.append(date)
    if description is not None:
        fields.append("description=?")
        values.append(description)
    if not fields:
        return  # Nothing to update
    values.append(expense_id)
    sql = f"UPDATE expenses SET {', '.join(fields)} WHERE id=?"
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    """Delete an expense record and any associated group expense."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    cursor.execute("DELETE FROM group_expenses WHERE expense_id=?", (expense_id,))
    conn.commit()
    conn.close()

def fetch_expenses(filter_by=None, value=None):
    """
    Retrieve expense records.
    Optionally filter by a given column (e.g., 'category' or 'date').
    """
    conn = get_connection()
    cursor = conn.cursor()
    if filter_by and value:
        sql = f"SELECT * FROM expenses WHERE {filter_by}=?"
        cursor.execute(sql, (value,))
    else:
        cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_group_expense(expense_id, group_name, participants):
    """
    Add a group expense entry.
    
    Parameters:
      expense_id: The expense record ID to associate with this group expense.
      group_name: Name of the group.
      participants: Comma-separated list of participant names.
    
    Calculates the individual share by dividing the expense amount equally.
    """
    conn = get_connection()
    cursor = conn.cursor()
    # Retrieve the expense amount
    cursor.execute("SELECT amount FROM expenses WHERE id=?", (expense_id,))
    result = cursor.fetchone()
    if result:
        amount = result[0]
        # Split the expense equally among participants
        participant_list = [p.strip() for p in participants.split(',') if p.strip()]
        num_participants = len(participant_list)
        individual_share = amount / num_participants if num_participants > 0 else 0
        cursor.execute('''
            INSERT INTO group_expenses (expense_id, group_name, participants, individual_share)
            VALUES (?, ?, ?, ?)
        ''', (expense_id, group_name, participants, individual_share))
        conn.commit()
    conn.close()

def fetch_group_expenses(group_name):
    """
    Retrieve group expense records for a given group name.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM group_expenses WHERE group_name=?", (group_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows
