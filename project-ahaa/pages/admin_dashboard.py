import streamlit as st

def render_admin_dashboard():
    """Renders the dashboard for logged-in admin users."""
    role = st.session_state.get("user_role")
    name = st.session_state.get("user_name", "Admin")
    
    st.markdown(f"<div class='main-header'>⚙️ Admin Dashboard</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>Welcome, {name}! Start managing the database and data sources.</div>", unsafe_allow_html=True)
    st.info(f"👤 Role: {role.capitalize()}")

    st.markdown("### 📋 Admin Quick Tools")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚙️ Admin Panel (Ingestion)", use_container_width=True):
            st.session_state["current_view"] = "⚙️ Admin Panel"
            st.rerun()
    with col2:
        if st.button("📚 Explore Projects", use_container_width=True):
            st.session_state["current_view"] = "📚 Explore Projects"
            st.rerun()

    st.markdown("### 🚀 Content Tools")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💡 Submit Idea", use_container_width=True):
            st.session_state["current_view"] = "💡 Submit Idea"
            st.rerun()
    with col2:
        if st.button("🔗 Knowledge Graph", use_container_width=True):
            st.session_state["current_view"] = "🔗 Knowledge Graph"
            st.rerun()
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            from auth.auth_utils import logout
            logout()
            st.rerun()

    st.markdown("---")
    st.info("👈 Use the sidebar for manual navigation between your dashboard and search tools.")
