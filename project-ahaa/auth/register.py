import streamlit as st
from database.db import create_user, get_user_by_email

def render_register_page():
    """Renders the registration interface on the Streamlit app."""
    st.markdown("<div class='main-header'>📝 Project AHAA Registration</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Create an account to get started.</div>", unsafe_allow_html=True)
    
    with st.form("register_form"):
        name = st.text_input("👤 Full Name", placeholder="Enter your full name")
        email = st.text_input("📧 Email Address", placeholder="e.g. student@test.com")
        password = st.text_input("🔑 Password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("🔑 Confirm Password", type="password", placeholder="Re-enter your password")
        role = st.selectbox("👤 Select Role", ["student", "admin"], help="Admins have access to data ingestion tools.")
        
        submitted = st.form_submit_button("Create Account", use_container_width=True)

    if submitted:
        if name and email and password and confirm_password:
            if password != confirm_password:
                st.error("❌ Passwords do not match.")
            elif len(password) < 6:
                st.warning("⚠️ Password must be at least 6 characters long.")
            elif get_user_by_email(email):
                st.error("❌ Email already registered. Please login instead.")
            else:
                if create_user(name, email, password, role):
                    st.success("✅ Registration successful! Please switch to the Login tab.")
                else:
                    st.error("❌ Something went wrong. Please try again later.")
        else:
            st.warning("⚠️ Please fill in all fields.")
