import streamlit as st
import sys
from pathlib import Path

# ─── Make project root importable ─────────────────────────────────────────────
project_root = Path(__file__).parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
# ──────────────────────────────────────────────────────────────────────────────

from backend.auth import register, login
from backend.expenses import add_expense, fetch_expenses, update_expense, delete_expense
from backend.analytics import monthly_summary, yearly_summary, category_trend
from backend.group import (
    list_user_groups,
    create_group,
    add_group_expense,
    compute_group_balances
)
from backend.visuals import plot_monthly, plot_category, plot_yearly

st.set_page_config(page_title='Dollar Bill Tracker', layout="wide")

# ─── Custom CSS ──────────────────────────────────────────
st.markdown(
    """
    <style>
    .main .block-container{
        max-width: 90%;
        margin: 0 auto;
        padding: 1.5rem;
        background-color: #f0f8ff;
    }
    /* Remove default Streamlit padding */
    .main {
        padding-top: 1rem;
    }
    /* Remove extra padding from the content area */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 1rem;
        padding-left: 0;
        padding-right: 0;
    }
    div.stButton > button {
        background-color: #1E90FF;
        color: white;
        padding: 0.8em 1.2em;
        border: none;
        border-radius: 0.3em;
        font-size: 1em;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #0066CC;
    }
    /* Streamlit tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        width: 100%;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        flex: 1;
        min-width: 150px;
        font-size: 16px;
        white-space: pre-wrap;
        background-color: white;
        border-radius: 0;
        border-bottom: 1px solid #e0e0e0;
        padding: 15px 20px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E90FF !important;
        color: white !important;
        border-bottom: none !important;
    }
    /* Make tabs container full width */
    .stTabs {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ─── Authentication ───────────────────────────────────────────────────────────
if 'user_id' not in st.session_state:
    st.session_state.user_id   = None
    st.session_state.username  = None

if not st.session_state.user_id:
    st.markdown("<h1 style='text-align: center; color: #1E90FF;'>Welcome to Dollar Bill</h1>", unsafe_allow_html=True)
    mode     = st.selectbox('Mode', ['Login', 'Register'])
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button(mode):
        ok, msg = (login if mode == 'Login' else register)(username, password)
        if ok:
            st.session_state.user_id  = msg
            st.session_state.username = username
            st.success(f"Logged in as {username}")
            st.rerun()  # Force rerun to update the UI immediately
        else:
            st.error(msg)
    # No st.stop() or experimental_rerun(): Streamlit will rerun automatically
else:
    # ─── Main App ───────────────────────────────────────────────────────────────
    # Get user info from session state
    user_id = st.session_state.user_id
    username = st.session_state.username
    
    # Create tabs for navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Dashboard', 'Expenses', 'Analytics', 'Groups', 'Logout'])
    
    # Dashboard tab content
    with tab1:
        st.title('Dashboard')
        #st.write(f"Hello, **{username}**! What would you like to do today?")
        user_groups = list_user_groups(user_id)
        if user_groups:
            st.subheader('Your Groups')
            group_sel = st.selectbox('Select a group', user_groups)
            if st.button('Compute Balances'):
                bal = compute_group_balances(group_sel)
                st.subheader(f"Balances for {group_sel}")
                # Display balances in a cleaner format
                st.markdown("### Balance Summary")
                for person, amount in bal.items():
                    if amount > 0:
                        st.markdown(f"**{person}** should receive **${amount:.2f}**")
                    elif amount < 0:
                        st.markdown(f"**{person}** owes **${abs(amount):.2f}**")
                    else:
                        st.markdown(f"**{person}** is settled (no payment needed)")
        else:
            st.info("You're not in any groups yet.")
    
    # Expenses tab content
    with tab2:
        # Create tabs for expense actions
        expense_tab1, expense_tab2, expense_tab3 = st.tabs(["Add Expense", "View/Edit Expenses", "Delete Expense"])
        
        # Add expense tab
        with expense_tab1:
            st.header('Add New Expense')
            amt  = st.number_input('Amount', min_value=0.0, step=0.01, key='new_amt')
            cat  = st.text_input('Category', key='new_cat')
            date = st.date_input('Date', key='new_date')
            desc = st.text_input('Description', key='new_desc')
            if st.button('Add Expense', key='add_btn'):
                add_expense(user_id, amt, cat, date.isoformat(), desc)
                st.success('Expense added successfully!')
        
        # View and update expenses tab
        with expense_tab2:
            st.header('View and Update Expenses')
            
            # Fetch and display expenses
            expenses = fetch_expenses(user_id)
            
            if not expenses:
                st.info("You don't have any expenses yet.")
            else:
                # Create a selection box for expenses
                expense_options = [f"{e['date'].date()} - {e['category']} - ${e['amount']:.2f} - {e['description']}" for e in expenses]
                selected_expense_idx = st.selectbox("Select an expense to edit:", 
                                                   range(len(expense_options)), 
                                                   format_func=lambda x: expense_options[x])
                
                # Get the selected expense
                selected_expense = expenses[selected_expense_idx]
                
                # Create form for updating
                st.subheader("Update Expense")
                updated_amt = st.number_input('New Amount', 
                                           min_value=0.0, 
                                           step=0.01, 
                                           value=float(selected_expense['amount']),
                                           key='update_amt')
                updated_cat = st.text_input('New Category', 
                                         value=selected_expense['category'], 
                                         key='update_cat')
                updated_date = st.date_input('New Date', 
                                          value=selected_expense['date'].date(),
                                          key='update_date')
                updated_desc = st.text_input('New Description', 
                                          value=selected_expense['description'], 
                                          key='update_desc')
                
                if st.button('Update Expense', key='update_btn'):
                    # Convert ObjectId to string for the expense_id
                    expense_id = str(selected_expense['_id'])
                    
                    # Call update function
                    update_expense(
                        expense_id,
                        user_id,
                        amount=updated_amt,
                        category=updated_cat,
                        date_str=updated_date.isoformat(),
                        description=updated_desc
                    )
                    st.success("Expense updated successfully!")
                    st.rerun()  # Refresh to show updated data
        
        # Delete expense tab
        with expense_tab3:
            st.header('Delete Expense')
            
            # Fetch and display expenses for deletion
            expenses = fetch_expenses(user_id)
            
            if not expenses:
                st.info("You don't have any expenses to delete.")
            else:
                # Create a selection box for expenses
                expense_options = [f"{e['date'].date()} - {e['category']} - ${e['amount']:.2f} - {e['description']}" for e in expenses]
                delete_expense_idx = st.selectbox("Select an expense to delete:", 
                                                 range(len(expense_options)), 
                                                 format_func=lambda x: expense_options[x],
                                                 key='delete_select')
                
                # Get the selected expense
                expense_to_delete = expenses[delete_expense_idx]
                
                # Show expense details for confirmation
                st.markdown(f"""
                **You are about to delete this expense:**
                - Date: {expense_to_delete['date'].date()}
                - Category: {expense_to_delete['category']}
                - Amount: ${expense_to_delete['amount']:.2f}
                - Description: {expense_to_delete['description']}
                """)
                
                if st.button('Delete This Expense', key='delete_btn'):
                    # Convert ObjectId to string for the expense_id
                    expense_id = str(expense_to_delete['_id'])
                    
                    # Call delete function
                    delete_expense(expense_id, user_id)
                    st.success("Expense deleted successfully!")
                    st.rerun()  # Refresh to show updated data

    # Analytics tab content
    with tab3:
        st.header('Analytics')
        
        # Monthly Summary
        st.subheader('Monthly Summary')
        try:
            monthly_data = monthly_summary(user_id)
            if monthly_data and len(monthly_data) > 0:
                monthly_img = plot_monthly(monthly_data)
                st.image(monthly_img)
            else:
                st.info("No monthly data available yet. Add some expenses to see your monthly summary.")
        except Exception as e:
            st.error(f"Error displaying monthly chart: {str(e)}")
            st.info("Try adding more expense data to generate monthly charts.")
        
        # Yearly Summary
        st.subheader('Yearly Summary')
        try:
            yearly_data = yearly_summary(user_id)
            if yearly_data and len(yearly_data) > 0:
                yearly_img = plot_yearly(yearly_data)
                st.image(yearly_img)
            else:
                st.info("No yearly data available yet. Add some expenses to see your yearly summary.")
        except Exception as e:
            st.error(f"Error displaying yearly chart: {str(e)}")
            st.info("Try adding more expense data with different years to generate yearly charts.")
        
        # Category Breakdown
        st.subheader('Spending by Category')
        try:
            category_data = category_trend(user_id)
            if category_data and len(category_data) > 0:
                category_img = plot_category(category_data)
                st.image(category_img)
            else:
                st.info("No category data available yet. Add expenses with categories to see this breakdown.")
        except Exception as e:
            st.error(f"Error displaying category chart: {str(e)}")
            st.info("Try adding more expense data with different categories to generate category charts.")

    # Groups tab content
    with tab4:
        st.header('Group Management')

        # 1) Show groups you belong to
        

        # 2) Create a new group by username
        st.subheader('Create New Group')
        new_name    = st.text_input('Group Name', key='new_grp_name')
        new_members = st.text_input('Member Usernames (comma-separated)', key='new_grp_mems')
        if st.button('Create Group'):
            member_usernames = [u.strip() for u in new_members.split(',') if u.strip()]
            try:
                create_group(new_name, member_usernames)
                st.success(f"Group {new_name} created")
            except Exception as e:
                st.error(str(e))

        # 3) Add an expense to a group (you as payer)
        if user_groups:
            st.subheader('Add Group Expense')
            grp_for_exp = st.selectbox('Group', user_groups, key='grp_exp')
            amt_g   = st.number_input('Amount', min_value=0.0, step=0.01, key='g_amt')
            cat_g   = st.text_input('Category', key='g_cat')
            date_g  = st.date_input('Date', key='g_date')
            desc_g  = st.text_input('Description', key='g_desc')
            if st.button('Add Group Expense'):
                try:
                    add_group_expense(
                        grp_for_exp,
                        username,
                        amt_g,
                        cat_g,
                        date_g.isoformat(),
                        desc_g
                    )
                    st.success('Group expense added')
                except Exception as e:
                    st.error(str(e))

    # Logout tab content
    with tab5:
        if st.button('Confirm Logout', key='confirm_logout'):
            st.session_state.clear()
            st.rerun()  # Force rerun to update the UI immediately
