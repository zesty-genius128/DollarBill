import sys
from database import (
    create_tables, add_expense, update_expense, delete_expense, 
    fetch_expenses, add_group_expense, fetch_group_expenses
)
from analytics import get_monthly_summary, get_yearly_summary, get_overall_trends
from insights import generate_contextual_summary

def print_expenses(expenses):
    """Helper function to neatly print expense records."""
    print("ID\tAmount\tCategory\tDate\t\tDescription")
    print("--\t------\t--------\t----\t\t-----------")
    for row in expenses:
        print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}")

def print_group_expenses(expenses):
    """Helper function to print group expense details."""
    print("ID\tExpense_ID\tGroup\tParticipants\tIndividual Share")
    print("--\t----------\t-----\t------------\t----------------")
    for row in expenses:
        print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]:.2f}")

def main():
    # Ensure the database tables are created at startup
    create_tables()
    while True:
        print("\n=== DollarBill Expense Tracker Menu ===")
        print("1. Add Expense")
        print("2. Add Group Expense")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. View All Expenses")
        print("6. Monthly Summary")
        print("7. Yearly Summary")
        print("8. View Overall Trends")
        print("9. Get AI Insights")
        print("10. View Group Expenses by Group Name")
        print("11. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            try:
                amount = float(input("Enter amount: "))
                category = input("Enter category: ")
                date = input("Enter date (YYYY-MM-DD): ")
                description = input("Enter description: ")
                add_expense(amount, category, date, description)
                print("Expense added successfully.")
            except Exception as e:
                print("Error adding expense:", e)
                
        elif choice == '2':
            try:
                amount = float(input("Enter amount for group expense: "))
                category = input("Enter category: ")
                date = input("Enter date (YYYY-MM-DD): ")
                description = input("Enter description: ")
                add_expense(amount, category, date, description)
                
                # Retrieve the last inserted expense ID using sqlite3.
                import sqlite3
                conn = sqlite3.connect("expenses.db")
                cursor = conn.cursor()
                cursor.execute("SELECT last_insert_rowid()")
                expense_id = cursor.fetchone()[0]
                conn.close()

                group_name = input("Enter group name: ")
                participants = input("Enter participants (comma-separated): ")
                add_group_expense(expense_id, group_name, participants)
                print("Group expense added successfully.")
            except Exception as e:
                print("Error adding group expense:", e)
                
        elif choice == '3':
            try:
                expense_id = int(input("Enter expense ID to update: "))
                print("Leave blank if no change is needed for a field.")
                amount_input = input("Enter new amount: ")
                amount = float(amount_input) if amount_input else None
                category = input("Enter new category: ") or None
                date = input("Enter new date (YYYY-MM-DD): ") or None
                description = input("Enter new description: ") or None
                update_expense(expense_id, amount, category, date, description)
                print("Expense updated successfully.")
            except Exception as e:
                print("Error updating expense:", e)
                
        elif choice == '4':
            try:
                expense_id = int(input("Enter expense ID to delete: "))
                delete_expense(expense_id)
                print("Expense deleted successfully.")
            except Exception as e:
                print("Error deleting expense:", e)
                
        elif choice == '5':
            expenses = fetch_expenses()
            if expenses:
                print_expenses(expenses)
            else:
                print("No expenses found.")
                
        elif choice == '6':
            try:
                month = input("Enter month (MM): ")
                year = input("Enter year (YYYY): ")
                df = get_monthly_summary(month, year)
                if not df.empty:
                    print("\nMonthly Summary:")
                    print(df.to_string(index=False))
                else:
                    print("No data found for the specified month and year.")
            except Exception as e:
                print("Error generating monthly summary:", e)
                
        elif choice == '7':
            try:
                year = input("Enter year (YYYY): ")
                df = get_yearly_summary(year)
                if not df.empty:
                    print("\nYearly Summary:")
                    print(df.to_string(index=False))
                else:
                    print("No data found for the specified year.")
            except Exception as e:
                print("Error generating yearly summary:", e)
                
        elif choice == '8':
            try:
                df = get_overall_trends()
                if not df.empty:
                    print("\nOverall Trends:")
                    print(df.to_string(index=False))
                else:
                    print("No expense data available for overall trends.")
            except Exception as e:
                print("Error generating overall trends:", e)
                
        elif choice == '9':
            try:
                user_query = input("Enter any specific query (e.g., 'monthly', 'group', 'budget') or leave blank: ")
                summary = generate_contextual_summary(user_query)
                print("\n=== AI Insights ===")
                print(summary)
            except Exception as e:
                print("Error generating AI insights:", e)
                
        elif choice == '10':
            try:
                group_name = input("Enter group name: ")
                group_expenses = fetch_group_expenses(group_name)
                if group_expenses:
                    print_group_expenses(group_expenses)
                else:
                    print("No group expenses found for the given group name.")
            except Exception as e:
                print("Error retrieving group expenses:", e)
                
        elif choice == '11':
            print("Exiting DollarBill Expense Tracker. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
