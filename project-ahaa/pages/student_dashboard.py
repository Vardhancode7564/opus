import streamlit as st

def render_student_dashboard():
    """Renders the dashboard for logged-in students."""
    role = st.session_state.get("user_role")
    name = st.session_state.get("user_name", "Student")
    
    st.markdown(f"<div class='main-header'>🎓 Student Dashboard</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-header'>Welcome, {name}! Start exploring academic project ideas.</div>", unsafe_allow_html=True)
    st.info(f"👤 Role: {role.capitalize()}")

    st.markdown("### 🚀 Quick Access")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💡 Submit Idea", use_container_width=True):
            st.session_state["current_view"] = "💡 Submit Idea"
            st.rerun()
    with col2:
        if st.button("📚 Explore Projects", use_container_width=True):
            st.session_state["current_view"] = "📚 Explore Projects"
            st.rerun()
    with col3:
        if st.button("🔗 Knowledge Graph", use_container_width=True):
            st.session_state["current_view"] = "🔗 Knowledge Graph"
            st.rerun()
    
    st.markdown("---")
    st.info("👈 Use the sidebar for manual navigation between your dashboard and search tools.")
