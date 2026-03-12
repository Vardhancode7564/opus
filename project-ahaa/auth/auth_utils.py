import streamlit as st

def is_logged_in():
    """Checks if a user is logged into the session."""
    return st.session_state.get("logged_in", False)

def get_user_role():
    """Retrieves the role of the logged-in user."""
    return st.session_state.get("user_role", None)

def get_user_name():
    """Retrieves the name of the logged-in user."""
    return st.session_state.get("user_name", "User")

def logout():
    """Clears the session state and logs the user out."""
    # Clear ALL session state keys to ensure data from previous user isn't leaked
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def check_admin_permission():
    """Stops execution if the user is not an admin."""
    if st.session_state.get("user_role") != "admin":
        st.error("🚫 Access Denied: You do not have permission to view this page or perform this action.")
        st.stop()
