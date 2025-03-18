import sqlite3
import pandas as pd
from database import DATABASE_NAME

def get_ai_summary():
    """
    Simulate an AI-generated summary of expenses.
    Returns a textual summary of overall spending and trends.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    query = "SELECT date, amount, category FROM expenses"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        return "No expenses found to generate a summary."

    # Calculate total expense
    total_expense = df['amount'].sum()

    # Determine the category with the highest spending
    category_summary = df.groupby('category')['amount'].sum()
    top_category = category_summary.idxmax()
    top_category_amount = category_summary.max()

    # Calculate average expense per transaction
    avg_expense = df['amount'].mean()

    summary = (
        f"Your total expenses amount to ${total_expense:.2f}. "
        f"You spent the most on '{top_category}' with a total of ${top_category_amount:.2f}. "
        f"On average, each transaction is about ${avg_expense:.2f}."
    )
    return summary
