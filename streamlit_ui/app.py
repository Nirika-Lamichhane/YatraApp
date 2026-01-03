import streamlit as st
from utils.api import login_user, fetch_data

# 1. Page Config (MUST be the first streamlit command)
st.set_page_config(page_title="Travel Planner", layout="centered")

# 2. Check Login State
if "access_token" not in st.session_state:
    # --- LOGIN SCREEN ---
    st.title("🔐 Travel App Login")
    
    with st.form("login_form"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Login", use_container_width=True):
            res = login_user(u, p)
            if res:
                st.session_state.access_token = res['access']
                st.rerun()
            else:
                st.error("Invalid Credentials")
else:
    # --- LOGGED IN: Custom Sidebar ---
    st.sidebar.success("Logged In!")
    if st.sidebar.button("Logout"):
        del st.session_state.access_token
        st.rerun()

    # Now we define the navigation for the sub-pages
    # This prevents the "3 buttons" from showing up on the login screen
    pg = st.navigation([
        st.Page("pages/1_Dashboard.py", title="Dashboard", icon="📊"),
        st.Page("pages/2_AI_Assistant.py", title="AI Assistant", icon="🤖")
    ])
    pg.run()