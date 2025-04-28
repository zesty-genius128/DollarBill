# backend/visuals.py

import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd

def plot_category(data):
    """
    Bar chart of total spending per category.
    Args:
      data: list of dicts or DataFrame with columns ['_id', 'total'].
    Returns:
      BytesIO PNG buffer.
    """
    # Normalize to DataFrame
    df = pd.DataFrame(data) if isinstance(data, list) else data.copy()

    # Unwrap dict _id if needed
    if '_id' in df.columns and df['_id'].apply(lambda x: isinstance(x, dict)).any():
        df['_id'] = df['_id'].apply(lambda x: next(iter(x.values())) if isinstance(x, dict) else x)

    # Plot
    fig, ax = plt.subplots()
    ax.bar(df['_id'], df['total'])
    ax.set_xlabel('Category')
    ax.set_ylabel('Total Spent')
    ax.set_title('Spending by Category')
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()

    # Buffer
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf


def plot_monthly(data):
    """
    Line chart of total spending over time periods (e.g., monthly).
    Args:
      data: list of dicts or DataFrame with columns ['_id', 'total'], where '_id'
            may be a dict like {'year':2025,'month':4} or a simple label.
    Returns:
      BytesIO PNG buffer.
    """
    # Normalize
    df = pd.DataFrame(data) if isinstance(data, list) else data.copy()

    # Build a string label for each period
    if '_id' in df.columns and df['_id'].apply(lambda x: isinstance(x, dict)).any():
        df['period'] = df['_id'].apply(
            lambda x: f"{x.get('year')}-{int(x.get('month')):02d}"
        )
    else:
        df['period'] = df['_id'].astype(str)

    # Sort by period lexicographically (YYYY-MM works)
    df = df.sort_values('period')

    # Plot
    fig, ax = plt.subplots()
    ax.plot(df['period'], df['total'], marker='o')
    ax.set_xlabel('Period')
    ax.set_ylabel('Total Spent')
    ax.set_title('Spending Trend Over Time')
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()

    # Buffer
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf
