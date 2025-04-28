import streamlit as st
import sys
from pathlib import Path

# ─── Make project root importable ─────────────────────────────────────────────
project_root = Path(__file__).parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
# ──────────────────────────────────────────────────────────────────────────────

from backend.auth import register, login
from backend.expenses import add_expense, fetch_expenses
from backend.analytics import monthly_summary, yearly_summary, category_trend
from backend.group import (
    list_user_groups,
    create_group,
    add_group_expense,
    compute_group_balances
)
from backend.visuals import plot_monthly, plot_category

st.set_page_config(page_title='Dollar Bill Tracker')

# ─── Authentication ───────────────────────────────────────────────────────────
if 'user_id' not in st.session_state:
    st.session_state.user_id   = None
    st.session_state.username  = None

if not st.session_state.user_id:
    st.title('Welcome to Dollar Bill')
    mode     = st.selectbox('Mode', ['Login', 'Register'])
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button(mode):
        ok, msg = (login if mode == 'Login' else register)(username, password)
        if ok:
            st.session_state.user_id  = msg
            st.session_state.username = username
            st.success(f"Logged in as {username}")
        else:
            st.error(msg)
    # No st.stop() or experimental_rerun(): Streamlit will rerun automatically
else:
    # ─── Main App ───────────────────────────────────────────────────────────────
    st.sidebar.title('Navigation')
    page    = st.sidebar.radio('', ['Dashboard', 'Expenses', 'Analytics', 'Groups', 'Logout'])
    user_id = st.session_state.user_id
    username = st.session_state.username

    if page == 'Logout':
        if st.sidebar.button('Confirm Logout'):
            st.session_state.clear()

    elif page == 'Dashboard':
        st.title('Dashboard')
        st.write(f"Hello, **{username}**! What would you like to do today?")

    elif page == 'Expenses':
        st.header('Add Individual Expense')
        amt  = st.number_input('Amount', min_value=0.0, step=0.01)
        cat  = st.text_input('Category')
        date = st.date_input('Date')
        desc = st.text_input('Description')
        if st.button('Add Expense'):
            add_expense(user_id, amt, cat, date.isoformat(), desc)
            st.success('Expense added')

        st.subheader('Your Expenses')
        for e in fetch_expenses(user_id):
            st.write(f"{e['date'].date()}: {e['category']} - ${e['amount']}")

    elif page == 'Analytics':
        st.header('Analytics')
        st.subheader('Monthly Summary')
        st.image(plot_monthly(monthly_summary(user_id)))
        st.subheader('Yearly Summary (raw data)')
        st.json(yearly_summary(user_id))
        st.subheader('Spending by Category')
        st.image(plot_category(category_trend(user_id)))

    elif page == 'Groups':
        st.header('Group Management')

        # 1) Show groups you belong to
        user_groups = list_user_groups(user_id)
        if user_groups:
            st.subheader('Your Groups')
            group_sel = st.selectbox('Select a group', user_groups)
            if st.button('Compute Balances'):
                bal = compute_group_balances(group_sel)
                st.subheader(f"Balances for “{group_sel}”")
                st.json(bal)
        else:
            st.info("You’re not in any groups yet.")

        # 2) Create a new group by username
        st.subheader('Create New Group')
        new_name    = st.text_input('Group Name', key='new_grp_name')
        new_members = st.text_input('Member Usernames (comma-separated)', key='new_grp_mems')
        if st.button('Create Group'):
            member_usernames = [u.strip() for u in new_members.split(',') if u.strip()]
            try:
                create_group(new_name, member_usernames)
                st.success(f"Group “{new_name}” created")
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
