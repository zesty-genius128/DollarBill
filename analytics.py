import sqlite3
import pandas as pd
from database import DATABASE_NAME

def get_monthly_summary(month, year):
    """
    Generate a monthly summary by category.
    Groups expenses for a given month and year.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    query = """
    SELECT category, SUM(amount) as total
    FROM expenses
    WHERE strftime('%m', date)=? AND strftime('%Y', date)=?
    GROUP BY category
    """
    month_str = f"{int(month):02d}"
    year_str = str(year)
    df = pd.read_sql_query(query, conn, params=(month_str, year_str))
    conn.close()
    return df

def get_yearly_summary(year):
    """
    Generate a yearly summary, aggregating total expenses per month.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    query = """
    SELECT strftime('%m', date) as month, SUM(amount) as total
    FROM expenses
    WHERE strftime('%Y', date)=?
    GROUP BY month
    """
    year_str = str(year)
    df = pd.read_sql_query(query, conn, params=(year_str,))
    conn.close()
    return df

def get_overall_trends():
    """
    Provide overall expense trends by category.
    Useful for high-level financial planning.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    query = """
    SELECT category, SUM(amount) as total
    FROM expenses
    GROUP BY category
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
