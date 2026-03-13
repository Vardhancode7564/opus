import streamlit as st
from database.db import create_user, get_user_by_email

def render_register_page():
    """Renders the registration interface on the Streamlit app."""
    # Headers moved to app.py for layout consistency
    with st.form("register_form"):
        name = st.text_input("👤 Full Name", placeholder="Enter your full name")
        email = st.text_input("📧 Email Address", placeholder="e.g. student@test.com")
        password = st.text_input("🔑 Password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("🔑 Confirm Password", type="password", placeholder="Re-enter your password")
        
        submitted = st.form_submit_button("Join AHAA", use_container_width=True)

    if submitted:
        if name and email and password and confirm_password:
            role = "student" # Default role for all registrations
            if password != confirm_password:
                st.error("❌ Passwords do not match.")
            elif len(password) < 6:
                st.warning("⚠️ Password must be at least 6 characters long.")
            elif get_user_by_email(email):
                st.error("❌ Email already registered. Please login instead.")
            else:
                if create_user(name, email, password, role):
                    # Clear existing session data before setting new user context
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                        
                    # Automatically log in the user after registration
                    st.session_state["logged_in"] = True
                    st.session_state["user_role"] = role
                    st.session_state["user_name"] = name
                    st.session_state["user_email"] = email
                    
                    st.success(f"✅ Registration successful! Welcome, {name}!")
                    st.rerun() # Refresh app to bypass login screens
                else:
                    st.error("❌ Something went wrong. Please try again later.")
        else:
            st.warning("⚠️ Please fill in all fields.")
