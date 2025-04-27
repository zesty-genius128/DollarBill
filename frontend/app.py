import streamlit as st
from backend.auth import login, register

st.title("Dollar Bill – Expense Tracker")

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if not st.session_state.user_id:
    option = st.selectbox("Choose", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button(option):
        success, msg_or_id = (login if option == "Login" else register)(username, password)
        st.success(msg_or_id) if success else st.error(msg_or_id)
        if success and option == "Login":
            st.session_state.user_id = msg_or_id
