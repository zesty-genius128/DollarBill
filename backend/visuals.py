# backend/visuals.py

import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd

def plot_monthly(data):
    """
    Line chart of total spending per month.
    """
    df = pd.DataFrame(data) if isinstance(data, list) else data.copy()
    df['period'] = df['_id'].apply(
        lambda x: f"{x['year']}-{int(x['month']):02d}" if isinstance(x, dict) else str(x)
    )
    df = df.sort_values('period')

    fig, ax = plt.subplots()
    ax.plot(df['period'], df['total'], marker='o', label='Total')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Spent')
    ax.set_title('Monthly Spending Trend')
    ax.legend()
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf


def plot_yearly(data):
    """
    Bar chart of total spending per year.
    """
    df = pd.DataFrame(data) if isinstance(data, list) else data.copy()
    df['year'] = df['_id'].apply(lambda x: x['year'] if isinstance(x, dict) else x)
    df = df.sort_values('year')

    fig, ax = plt.subplots()
    ax.bar(df['year'].astype(str), df['total'], label='Total')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Spent')
    ax.set_title('Yearly Spending')
    ax.legend()
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf


def plot_category(data):
    """
    Pie chart of spending by category.
    """
    df = pd.DataFrame(data) if isinstance(data, list) else data.copy()
    df['category'] = df['_id'].apply(
        lambda x: x['category'] if isinstance(x, dict) else x
    )
    labels = df['category']
    sizes  = df['total']

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        sizes,
        autopct='%1.1f%%',
        startangle=90
    )
    ax.set_title('Spending by Category')
    ax.axis('equal')
    ax.legend(
        wedges,
        labels,
        title='Category',
        loc='center left',
        bbox_to_anchor=(1, 0.5)
    )
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf
