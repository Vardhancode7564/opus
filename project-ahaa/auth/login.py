import streamlit as st
from database.db import get_user_by_email, verify_password

def render_login_page():
    """Renders the login interface on the Streamlit app."""
    # Headers moved to app.py for layout consistency
    with st.form("login_form"):
        email = st.text_input("📧 Email Address", placeholder="e.g., student@test.com")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Start Exploring Ideas", use_container_width=True)

    if submitted:
        if email and password:
            user_record = get_user_by_email(email)
            if user_record and verify_password(password, user_record["password_hash"]):
                # Clear existing session data before setting new user context
                # This prevents data leak from a previous session that wasn't properly closed
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                    
                st.session_state["logged_in"] = True
                st.session_state["user_role"] = user_record["role"]
                st.session_state["user_name"] = user_record["name"]
                st.session_state["user_email"] = user_record["email"]
                st.success(f"✅ Welcome back, {user_record['name']}!")
                st.rerun()
            else:
                st.error("❌ Invalid email or password. Please try again.")
        else:
            st.warning("⚠️ Please fill in all fields.")
