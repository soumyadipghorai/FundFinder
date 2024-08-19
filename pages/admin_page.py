import streamlit as st
from utils.auth import check_credentials

st.title("Admin Log in")

if not st.session_state.authenticated:
    st.write("Securely log in to manage and oversee the FundFinder application.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login") : 
        if check_credentials(username, password):
            st.session_state.authenticated = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")
else : 
    st.write("Securely log out to manage and oversee the FundFinder application.")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.success("Log out successful!")