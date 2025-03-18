import sqlite3
import pandas as pd
import numpy as np
from database import DATABASE_NAME

def detect_anomalies(z_threshold=2.0):
    """
    Detect expense anomalies based on a z-score method.
    An expense is flagged if its z-score exceeds the threshold.
    
    Returns:
      DataFrame of anomalous expense records.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    query = "SELECT * FROM expenses"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        return pd.DataFrame()  # No data available
    
    # Compute z-scores for the 'amount' field.
    mean_amount = df['amount'].mean()
    std_amount = df['amount'].std()
    if std_amount == 0:
        return pd.DataFrame()  # No variation, hence no anomalies.
    
    df['z_score'] = (df['amount'] - mean_amount) / std_amount
    anomalies = df[df['z_score'].abs() > z_threshold]
    return anomalies

def predict_future_spending():
    """
    Predict future spending using linear regression on monthly totals.
    Returns:
      A predicted expense total for the next month (float) or None if insufficient data.
    """
    from sklearn.linear_model import LinearRegression
    conn = sqlite3.connect(DATABASE_NAME)
    query = """
        SELECT strftime('%Y-%m', date) as period, SUM(amount) as total
        FROM expenses
        GROUP BY period
        ORDER BY period
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty or len(df) < 2:
        return None  # Not enough data to perform prediction.
    
    # Convert the period into a sequential time index.
    df = df.reset_index(drop=True)
    df['time_index'] = np.arange(len(df))
    
    X = df[['time_index']]
    y = df['total']
    
    model = LinearRegression()
    model.fit(X, y)
    
    next_index = np.array([[df['time_index'].iloc[-1] + 1]])
    predicted = model.predict(next_index)
    return predicted[0]

def generate_contextual_summary(user_input=None):
    """
    Generate an interactive and contextual summary of the expense data.
    
    Optionally tailors the summary if a user query (e.g., about "monthly", "group", or "budget")
    is provided.
    
    Returns:
      A string summary including total expenses, anomaly detection results,
      predictive insights, and contextual recommendations.
    """
    # Anomaly detection results
    anomalies = detect_anomalies()
    
    # Predict next month's spending.
    predicted_next = predict_future_spending()
    
    # Get overall total expenses.
    conn = sqlite3.connect(DATABASE_NAME)
    query_total = "SELECT SUM(amount) as total FROM expenses"
    total_df = pd.read_sql_query(query_total, conn)
    conn.close()
    total_expense = total_df['total'][0] if not total_df.empty and total_df['total'][0] is not None else 0.0
    
    # Build the basic summary.
    summary = f"Your total recorded expenses are ${total_expense:.2f}.\n"
    if not anomalies.empty:
        summary += (f"Anomaly Detection: {len(anomalies)} transaction(s) appear anomalous "
                    f"(e.g., transactions above ${anomalies['amount'].max():.2f}).\n")
    else:
        summary += "Anomaly Detection: No significant anomalies detected in your expenses.\n"
    
    if predicted_next is not None:
        summary += f"Predictive Insight: Based on your spending trend, your predicted total expense for next month is ${predicted_next:.2f}.\n"
    else:
        summary += "Predictive Insight: Not enough data to forecast next month's expenses.\n"
    
    # Add interactive contextual notes based on the user's query.
    if user_input:
        lower_input = user_input.lower()
        if "monthly" in lower_input:
            summary += "Contextual Note: Your monthly spending appears stable. Consider maintaining a consistent budget.\n"
        elif "group" in lower_input:
            summary += "Contextual Note: For group expenses, ensure prompt settlements among participants.\n"
        elif "budget" in lower_input:
            summary += "Contextual Note: A detailed budgeting plan might help curb overspending in high-expense categories.\n"
        else:
            summary += "Contextual Note: Regular monitoring of your spending can help optimize your financial planning.\n"
    else:
        summary += "Contextual Note: Regular review of your expenses can reveal trends and opportunities for savings.\n"
    
    return summary

# Example usage:
if __name__ == "__main__":
    print("=== Anomaly Detection ===")
    anomalies_df = detect_anomalies()
    if anomalies_df.empty:
        print("No anomalies found.")
    else:
        print(anomalies_df)
    
    print("\n=== Predictive Insight ===")
    predicted_value = predict_future_spending()
    if predicted_value is not None:
        print(f"Predicted spending for next month: ${predicted_value:.2f}")
    else:
        print("Not enough data to predict future spending.")
    
    print("\n=== Contextual Summary ===")
    print(generate_contextual_summary("Tell me about my monthly spending."))
