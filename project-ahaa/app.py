"""
PROJECT AHAA - AI Hub for Academic Advancement
Main Streamlit Application with RBAC
"""

import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import logging
import streamlit.components.v1 as components

# Import Authentication and DB modules
from database.db import init_db
from auth.auth_utils import is_logged_in, logout, get_user_role, get_user_name, check_admin_permission
from auth.login import render_login_page
from auth.register import render_register_page
from pages.student_dashboard import render_student_dashboard
from pages.admin_dashboard import render_admin_dashboard

# Initialize DB on startup
init_db()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Project AHAA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-card h3 { margin: 0; font-size: 2rem; }
    .metric-card p { margin: 0; font-size: 0.9rem; opacity: 0.9; }
    .source-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        color: white;
    }
    .source-github { background-color: #4078c0; }
    .source-web { background-color: #2ecc71; }
    .source-admin { background-color: #e74c3c; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
    }
    /* Hide the top navigation menu (tabs like 'app', 'admin dashboard', etc.) */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    /* Hide the status/profile indicators at the top right if any */
    .stAppDeployButton, [data-testid="stStatusWidget"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ── ROUTING AND AUTHENTICATION ──────────────────────────────────────────────

# Initialize Session State for Search Results and Knowledge Graph persistence
if "search_results" not in st.session_state:
    st.session_state["search_results"] = None
if "current_idea" not in st.session_state:
    st.session_state["current_idea"] = None
if "last_suggestions" not in st.session_state:
    st.session_state["last_suggestions"] = None
if "current_view" not in st.session_state:
    st.session_state["current_view"] = "🏠 Home"

# 1. Start with Login or Register if not authenticated
if not is_logged_in():
    st.markdown("""
        <style>
            /* ── Reset Streamlit Chrome ── */
            header,
            [data-testid="stHeader"],
            [data-testid="stToolbar"],
            footer {
                display: none !important;
            }

            [data-testid="stSidebar"],
            .stSidebar {
                display: none !important;
                width: 0px !important;
            }

            /* ── Full-page dark background ── */
            .stApp {
                background-color: #0d1117 !important;
            }

            /* ── Outer wrapper: vertically + horizontally center the card ── */
            [data-testid="stAppViewBlockContainer"] {
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                min-height: 100vh !important;
                padding: 2rem 1rem !important;
            }

            /* ── The card itself ── */
            .main .block-container {
                width: 100% !important;
                max-width: 460px !important;
                padding: 2rem 2.5rem 2.5rem !important;
                background-color: #161b22 !important;
                border: 1px solid #30363d !important;
                border-radius: 14px !important;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.65) !important;
                margin: auto !important;
            }

            /* ── Force inner blocks to fill the card ── */
            [data-testid="stVerticalBlock"],
            [data-testid="stForm"] {
                width: 100% !important;
                max-width: 100% !important;
            }

            [data-baseweb="tab-panel"] {
                width: 100% !important;
                padding: 0 !important;
            }

            /* ── Header ── */
            .main-header {
                font-size: 1.9rem !important;
                font-weight: 700 !important;
                color: #8b5cf6 !important;
                -webkit-text-fill-color: #8b5cf6 !important;
                background: none !important;
                text-align: center !important;
                margin: 0 0 4px !important;
                padding: 0 !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                gap: 4px !important;
            }

            .header-icon {
                font-size: 2.6rem !important;
            }

            .sub-header {
                color: #8b949e !important;
                text-align: center !important;
                font-size: 0.88rem !important;
                line-height: 1.5 !important;
                margin: 0 0 20px !important;
                padding: 0 !important;
            }

            /* ── Tabs ── */
            [data-baseweb="tab-list"] {
                justify-content: center !important;
                gap: 24px !important;
                border-bottom: 2px solid #30363d !important;
                margin-bottom: 22px !important;
                padding: 0 !important;
            }

            [data-baseweb="tab"] {
                color: #768390 !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
                padding: 8px 4px 12px !important;
                border-bottom: 2px solid transparent !important;
                background: none !important;
            }

            [aria-selected="true"] {
                color: #ef4444 !important;
                border-bottom: 2px solid #ef4444 !important;
            }

            /* ── Form container ── */
            [data-testid="stForm"] {
                border: 1px solid #30363d !important;
                background-color: #0d1117 !important;
                padding: 28px 28px 32px !important;
                border-radius: 10px !important;
            }

            /* ── Labels ── */
            label,
            [data-testid="stWidgetLabel"] p {
                color: #cdd9e5 !important;
                font-size: 0.9rem !important;
                font-weight: 500 !important;
                margin-bottom: 4px !important;
                text-align: left !important;
            }

            /* ── Input fields ── */
            div[data-baseweb="input"] {
                background-color: #1c2128 !important;
                border: 1px solid #444c56 !important;
                border-radius: 6px !important;
                transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
            }

            div[data-baseweb="input"]:focus-within {
                border-color: #58a6ff !important;
                box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.18) !important;
            }

            input {
                color: #adbac7 !important;
                font-size: 0.95rem !important;
                text-align: left !important;
            }

            input::placeholder {
                color: #484f58 !important;
            }

            /* ── Submit button ── */
            button[kind="primaryFormSubmit"] {
                width: 100% !important;
                background-color: transparent !important;
                border: 1px solid #58a6ff !important;
                color: #58a6ff !important;
                border-radius: 6px !important;
                font-weight: 600 !important;
                font-size: 0.9rem !important;
                letter-spacing: 0.08em !important;
                text-transform: uppercase !important;
                padding: 0.65rem 1rem !important;
                margin-top: 28px !important;
                transition: background-color 0.2s ease, color 0.2s ease, transform 0.15s ease !important;
            }

            button[kind="primaryFormSubmit"]:hover {
                background-color: rgba(88, 166, 255, 0.12) !important;
                color: #ffffff !important;
                transform: translateY(-1px) !important;
            }

            /* ── Tighten vertical spacing inside card ── */
            [data-testid="stVerticalBlock"] > div {
                padding-top: 0 !important;
                padding-bottom: 0 !important;
            }

            [data-testid="stVerticalBlock"] {
                gap: 2px !important;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='main-header'>
            <span class='header-icon'>🔓</span>
            Project AHAA Login
        </div>
    """, unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-header'>Research. Validate. Innovate.<br>"
        "Discover and search innovative ideas on AHAA.</div>",
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["🔒 Account Login", "📝 Join AHAA"])
    with tab1:
        render_login_page()
    with tab2:
        render_register_page()
    st.stop()  # Halt execution here if not logged in

# 2. Get User Context
user_role = get_user_role()
user_name = get_user_name()

# ── Sidebar Navigation ──────────────────────────────────────────────────────
st.sidebar.markdown(f"## 🎓 Project AHAA")
st.sidebar.markdown(f"*Welcome, {user_name}*")
st.sidebar.markdown(f"**Role: {user_role.capitalize()}**")
st.sidebar.markdown("---")

# Navigation options based on role
nav_options = ["🏠 Home", "💡 Submit Idea", "📚 Explore Projects", "🔗 Knowledge Graph"]
if user_role == "admin":
    nav_options.append("⚙️ Admin Panel")

# Initialize session state current_view if not exists or if it's not in nav_options
if "current_view" not in st.session_state:
    st.session_state["current_view"] = "🏠 Home"

# Sidebar radio for manual navigation
page = st.sidebar.radio(
    "Navigate",
    nav_options,
    key="nav_radio", # Added a key to help streamlit track the widget state
    index=nav_options.index(st.session_state["current_view"]) if st.session_state["current_view"] in nav_options else 0,
)

# Update session state if page is changed via sidebar
if page != st.session_state["current_view"]:
    st.session_state["current_view"] = page

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    logout()
    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# ROUTING CONTROLLER
# ══════════════════════════════════════════════════════════════════════════════

# ── PAGE: DASHBOARD (ROLE-BASED) ───────────────────────────────────────────
if st.session_state["current_view"] == "Dashboard":
    if user_role == "admin":
        render_admin_dashboard()
    else:
        render_student_dashboard()

# ── PAGE: HOME ──────────────────────────────────────────────────────────────
elif st.session_state["current_view"] == "🏠 Home":
    st.markdown('<div class="main-header">🎓 Project AHAA</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">AI Hub for Academic Advancement — '
        'Discover, Compare, and Innovate</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="metric-card"><h3>🔍</h3><p>Discover existing projects<br>before you build</p></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="metric-card"><h3>🤖</h3><p>AI-powered similarity<br>search & suggestions</p></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="metric-card"><h3>🔗</h3><p>Visualize project<br>relationships</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.markdown("### How It Works")
    st.markdown("""
    1. **Collect** — Project data is gathered from GitHub, web sources, and admin-uploaded reports.
    2. **Process** — Text is cleaned, and AI generates semantic embeddings for each project.
    3. **Search** — When you enter a project idea, we find the most similar existing projects using vector similarity.
    4. **Improve** — AI suggests innovative improvements to differentiate your idea.
    5. **Visualize** — Explore the knowledge graph showing relationships between projects.
    """)

    st.markdown("### Quick Start")
    st.info("👈 Use the sidebar to navigate. Start by **submitting your project idea** or **explore existing projects**.")

    # Show index stats if available
    try:
        from database.pinecone_db import get_index_stats
        stats = get_index_stats()
        if stats["total_vectors"] > 0:
            st.success(f"📊 **Database Status:** {stats['total_vectors']} projects indexed and ready for search.")
    except Exception:
        st.warning("⚠️ Database not connected. Go to Admin Panel to configure and populate data.")


# ── PAGE: SUBMIT IDEA ────────────────────────────────────────────────────────
elif st.session_state["current_view"] == "💡 Submit Idea":
    st.markdown("## 💡 Submit Your Project Idea")
    st.markdown("Enter your project idea below. We'll find similar existing projects and suggest improvements.")

    with st.form("idea_form"):
        idea_title = st.text_input("Project Title", placeholder="e.g., Smart Attendance System using Face Recognition")
        idea_description = st.text_area(
            "Project Description",
            placeholder="Describe your project idea in detail...",
            height=150,
        )
        idea_domain = st.selectbox(
            "Domain",
            [
                "Machine Learning / AI",
                "Web Development",
                "Mobile App",
                "IoT / Hardware",
                "Data Science",
                "Cybersecurity",
                "Blockchain",
                "Cloud Computing",
                "Game Development",
                "NLP / Text Processing",
                "Computer Vision",
                "Other",
            ],
        )
        submitted = st.form_submit_button("🔍 Find Similar Projects", use_container_width=True)

    if submitted and idea_title and idea_description:
        with st.spinner("Generating embeddings and searching..."):
            try:
                from processing.text_cleaner import prepare_project_text
                from processing.embedding_generator import generate_embedding
                from database.pinecone_db import search_similar
                from ai_engine.suggestion_generator import generate_suggestions

                # Prepare and embed the student idea
                idea_text = f"{idea_title} {idea_description} {idea_domain}"
                idea_embedding = generate_embedding(idea_text)

                # Search for similar projects
                similar = search_similar(idea_embedding, top_k=5)
                
                # Persistence: Store results in session state
                st.session_state["search_results"] = similar
                st.session_state["current_idea"] = {
                    "title": idea_title,
                    "description": idea_description,
                    "domain": idea_domain,
                    "embedding": idea_embedding
                }

                if similar:
                    st.markdown("### 🔎 Similar Projects Found")

                    # Results table
                    df = pd.DataFrame(similar)
                    display_cols = ["project_title", "description", "technologies", "source", "similarity_score", "project_link"]
                    available_cols = [c for c in display_cols if c in df.columns]
                    st.dataframe(
                        df[available_cols],
                        use_container_width=True,
                        column_config={
                            "project_title": st.column_config.TextColumn("Title", width="medium"),
                            "description": st.column_config.TextColumn("Description", width="large"),
                            "technologies": st.column_config.TextColumn("Tech"),
                            "source": st.column_config.TextColumn("Source"),
                            "similarity_score": st.column_config.ProgressColumn(
                                "Similarity", min_value=0, max_value=1, format="%.2f"
                            ),
                            "project_link": st.column_config.LinkColumn("Link"),
                        },
                    )

                    # Detailed cards
                    st.markdown("### 📋 Detailed Results")
                    for i, proj in enumerate(similar, 1):
                        source = proj.get("source", "unknown")
                        badge_class = f"source-{source}"
                        with st.expander(
                            f"#{i} — {proj.get('project_title', 'N/A')} "
                            f"(Score: {proj.get('similarity_score', 0):.2f})"
                        ):
                            st.markdown(f"**Source:** <span class='source-badge {badge_class}'>{source.upper()}</span>", unsafe_allow_html=True)
                            st.markdown(f"**Description:** {proj.get('description', 'N/A')}")
                            st.markdown(f"**Technologies:** {proj.get('technologies', 'N/A')}")
                            link = proj.get("project_link", "")
                            if link and link.startswith("http"):
                                st.markdown(f"🔗 [View Project]({link})")

                    # AI Suggestions
                    st.markdown("### 🤖 AI Improvement Suggestions")
                    with st.spinner("Generating AI suggestions..."):
                        student_idea = {
                            "title": idea_title,
                            "description": idea_description,
                            "domain": idea_domain,
                        }
                        suggestions = generate_suggestions(student_idea, similar)
                        st.session_state["last_suggestions"] = suggestions
                        st.markdown(suggestions)
                else:
                    st.info("No similar projects found in the database. Try adding projects via the Admin Panel first.")

            except Exception as e:
                st.error(f"Error during search: {e}")
                logger.exception("Search error")

    elif st.session_state.get("search_results"):
        # PERSISTENCE: Display stored results if user returns to this tab
        similar = st.session_state["search_results"]
        st.markdown(f"### 🔎 Last Results for: **{st.session_state['current_idea']['title']}**")
        
        df = pd.DataFrame(similar)
        display_cols = ["project_title", "description", "technologies", "source", "similarity_score", "project_link"]
        available_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(df[available_cols], use_container_width=True)
        
        if st.session_state.get("last_suggestions"):
            st.markdown("### 🤖 AI Improvement Suggestions")
            st.markdown(st.session_state["last_suggestions"])

    elif submitted:
        st.warning("Please fill in both the project title and description.")


# ── PAGE: EXPLORE PROJECTS ──────────────────────────────────────────────────
elif st.session_state["current_view"] == "📚 Explore Projects":
    st.markdown("## 📚 Explore Projects")
    st.markdown("Browse all projects collected from GitHub, web scraping, and admin uploads.")

    try:
        from database.pinecone_db import get_all_projects

        projects = get_all_projects(limit=200)

        if projects:
            # Source filter
            sources = sorted(set(p.get("source", "unknown") for p in projects))
            selected_sources = st.multiselect("Filter by Source", sources, default=sources)

            filtered = [p for p in projects if p.get("source", "unknown") in selected_sources]

            st.markdown(f"**Showing {len(filtered)} of {len(projects)} projects**")

            df = pd.DataFrame(filtered)
            display_cols = ["project_title", "description", "technologies", "source", "project_link"]
            available_cols = [c for c in display_cols if c in df.columns]

            st.dataframe(
                df[available_cols],
                use_container_width=True,
                column_config={
                    "project_title": st.column_config.TextColumn("Title", width="medium"),
                    "description": st.column_config.TextColumn("Description", width="large"),
                    "technologies": st.column_config.TextColumn("Tech"),
                    "source": st.column_config.TextColumn("Source"),
                    "project_link": st.column_config.LinkColumn("Link"),
                },
                height=500,
            )

            # Source distribution
            st.markdown("### 📊 Source Distribution")
            source_counts = pd.Series([p.get("source", "unknown") for p in filtered]).value_counts()
            st.bar_chart(source_counts)
        else:
            st.info("No projects in the database yet. Use the Admin Panel to add projects.")

    except Exception as e:
        st.error(f"Error loading projects: {e}")
        logger.exception("Explore error")


# ── PAGE: KNOWLEDGE GRAPH ────────────────────────────────────────────────────
elif st.session_state["current_view"] == "🔗 Knowledge Graph":
    st.markdown("## 🔗 Knowledge Graph")
    
    # Mode Selection: Full Graph vs. Idea Context
    graph_mode = st.radio(
        "Select Graph Scope",
        ["💡 My Idea Context", "🌐 Full Knowledge Base"],
        horizontal=True,
        help="Context mode shows your submitted idea and its direct relatives. Full mode shows all projects."
    )

    try:
        from database.pinecone_db import get_all_projects
        from processing.embedding_generator import generate_embeddings_batch, generate_embedding
        from processing.text_cleaner import prepare_project_text
        from visualization.graph_builder import (
            build_knowledge_graph,
            compute_similarity_matrix,
            render_graph_html,
        )
        from config import SIMILARITY_THRESHOLD

        projects = []
        if graph_mode == "💡 My Idea Context":
            if st.session_state.get("search_results") and st.session_state.get("current_idea"):
                # Use current idea as a "project" node
                idea = st.session_state["current_idea"]
                idea_node = {
                    "project_id": "current_user_idea",
                    "project_title": f"YOUR IDEA: {idea['title']}",
                    "description": idea["description"],
                    "source": "user_idea",
                    "embedding": idea["embedding"]
                }
                # Similar projects from search results
                similar_projs = st.session_state["search_results"]
                projects = [idea_node] + similar_projs
                st.info(f"Visualizing relationship between your idea and {len(similar_projs)} similar projects.")
            else:
                st.warning("No project remains in memory. Please submit an idea first in the '💡 Submit Idea' tab.")
                st.stop()
        else:
            projects = get_all_projects(limit=50) # Limit for performance

        if len(projects) < 2:
            st.info("Insufficient data to build a graph. Add more projects or submit an idea first.")
        else:
            threshold = st.slider(
                "Similarity Threshold (edges shown above this value)",
                min_value=0.3,
                max_value=0.95,
                value=0.4 if graph_mode == "💡 My Idea Context" else SIMILARITY_THRESHOLD,
                step=0.05,
            )

            if st.button("🔄 Generate Graph", use_container_width=True):
                with st.spinner("Building relationship graph..."):
                    # Extract embeddings
                    embeddings = []
                    for p in projects:
                        if "embedding" in p:
                            embeddings.append(p["embedding"])
                        else:
                            text = prepare_project_text(p)
                            embeddings.append(generate_embedding(text))

                    # Compute similarity matrix
                    sim_matrix = compute_similarity_matrix(embeddings)

                    # Build and render graph
                    G = build_knowledge_graph(projects, sim_matrix, threshold=threshold)
                    graph_path = os.path.join(os.getcwd(), "graph.html")
                    render_graph_html(G, graph_path)

                    # Display graph
                    if os.path.exists(graph_path):
                        with open(graph_path, "r", encoding="utf-8") as f:
                            html_content = f.read()
                        
                        st.components.v1.html(html_content, height=650, scrolling=True)
                        st.markdown(f"**Graph Stats:** {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
                    else:
                        st.error("Failed to generate graph file.")

                    # Legend
                    st.markdown("### Legend")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown("🔵 **GitHub** projects")
                    with col2:
                        st.markdown("🟢 **Web** scraped projects")
                    with col3:
                        st.markdown("🔴 **Admin** uploaded projects")

    except Exception as e:
        st.error(f"Error building knowledge graph: {e}")
        logger.exception("Graph error")


# ── PAGE: ADMIN PANEL ────────────────────────────────────────────────────────
elif st.session_state["current_view"] == "⚙️ Admin Panel":
    # SECURE THE ADMIN PANEL
    check_admin_permission()

    st.markdown("## ⚙️ Admin Panel")
    st.markdown("Manage data sources and project database.")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📤 Upload Files",
        "🐙 GitHub Scraper",
        "🌐 Web Scraper",
        "🗄️ Database",
    ])

    # ── Tab 1: File Upload ───────────────────────────────────────────────────
    with tab1:
        st.markdown("### Upload Project Reports")
        st.markdown("Supported formats: **PDF**, **DOCX**, **TXT**")

        uploaded_files = st.file_uploader(
            "Choose files",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
        )

        if uploaded_files and st.button("📥 Process & Store Uploads", key="upload_btn"):
            from admin.file_parser import parse_file
            from processing.text_cleaner import prepare_project_text
            from processing.embedding_generator import generate_embedding
            from database.pinecone_db import upsert_project

            progress_bar = st.progress(0)
            success_count = 0

            for i, file in enumerate(uploaded_files):
                try:
                    project = parse_file(file)
                    if project:
                        text = prepare_project_text(project)
                        embedding = generate_embedding(text)
                        upsert_project(project, embedding)
                        success_count += 1
                        st.success(f"✅ Processed: {file.name}")
                    else:
                        st.warning(f"⚠️ Could not extract text from: {file.name}")
                except Exception as e:
                    st.error(f"❌ Error processing {file.name}: {e}")

                progress_bar.progress((i + 1) / len(uploaded_files))

            st.info(f"Done! {success_count}/{len(uploaded_files)} files processed and stored.")

    # ── Tab 2: GitHub Scraper ────────────────────────────────────────────────
    with tab2:
        st.markdown("### GitHub Project Collector")

        github_query = st.text_input(
            "Search Query",
            value="student project",
            placeholder="e.g., machine learning final year project",
        )
        max_repos = st.slider("Max Repositories", 10, 200, 50)

        if st.button("🐙 Fetch from GitHub", key="github_btn"):
            from data_sources.github_scraper import search_github_repos
            from processing.text_cleaner import prepare_project_text
            from processing.embedding_generator import generate_embeddings_batch
            from database.pinecone_db import upsert_projects_batch

            with st.spinner(f"Fetching up to {max_repos} repos from GitHub..."):
                try:
                    repos = search_github_repos(query=github_query, max_results=max_repos)

                    if repos:
                        st.success(f"Found {len(repos)} repositories!")

                        # Show preview
                        preview_df = pd.DataFrame(repos)[["project_title", "description", "technologies", "project_link"]]
                        st.dataframe(preview_df, use_container_width=True, height=300)

                        # Generate embeddings and store
                        with st.spinner("Generating embeddings and storing..."):
                            texts = [prepare_project_text(r) for r in repos]
                            embeddings = generate_embeddings_batch(texts)
                            count = upsert_projects_batch(repos, embeddings)
                            st.success(f"✅ Stored {count} projects in database!")
                    else:
                        st.warning("No repositories found. Try a different search query.")
                except Exception as e:
                    st.error(f"Error: {e}")
                    logger.exception("GitHub scraper error")

    # ── Tab 3: Web Scraper ───────────────────────────────────────────────────
    with tab3:
        st.markdown("### Web Project Scraper")

        web_url = st.text_input(
            "Enter URL to Scrape",
            placeholder="https://example.com/project-ideas",
        )

        if web_url and st.button("🌐 Scrape Website", key="web_btn"):
            from data_sources.web_scraper import scrape_project_ideas
            from processing.text_cleaner import prepare_project_text
            from processing.embedding_generator import generate_embeddings_batch
            from database.pinecone_db import upsert_projects_batch

            with st.spinner(f"Scraping {web_url}..."):
                try:
                    projects = scrape_project_ideas(web_url)

                    if projects:
                        st.success(f"Found {len(projects)} project ideas!")

                        preview_df = pd.DataFrame(projects)[["project_title", "description", "technologies"]]
                        st.dataframe(preview_df, use_container_width=True, height=300)

                        with st.spinner("Generating embeddings and storing..."):
                            texts = [prepare_project_text(p) for p in projects]
                            embeddings = generate_embeddings_batch(texts)
                            count = upsert_projects_batch(projects, embeddings)
                            st.success(f"✅ Stored {count} projects in database!")
                    else:
                        st.warning("No projects extracted from this URL. The page structure may not be supported.")
                except Exception as e:
                    st.error(f"Error: {e}")
                    logger.exception("Web scraper error")

    # ── Tab 4: Database Management ───────────────────────────────────────────
    with tab4:
        st.markdown("### Database Management")

        try:
            from database.pinecone_db import get_index_stats, get_all_projects, delete_all

            stats = get_index_stats()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Projects Indexed", stats["total_vectors"])
            with col2:
                st.metric("Embedding Dimension", stats["dimension"])

            if st.button("🔄 Refresh Stats", key="refresh_stats"):
                st.rerun()

            st.markdown("---")
            st.markdown("### ⚠️ Danger Zone")
            if st.button("🗑️ Delete All Data", key="delete_all", type="secondary"):
                st.session_state["confirm_delete"] = True

            if st.session_state.get("confirm_delete"):
                st.warning("Are you sure? This will delete ALL projects from the database.")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Yes, delete everything", type="primary"):
                        delete_all()
                        st.session_state["confirm_delete"] = False
                        st.success("All data deleted.")
                        st.rerun()
                with col2:
                    if st.button("Cancel"):
                        st.session_state["confirm_delete"] = False
                        st.rerun()

        except Exception as e:
            st.error(f"Error connecting to database: {e}")
            st.info("Make sure your PINECONE_API_KEY is set in the .env file.")

# ── Footer ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<small>Built with ❤️ for Hackathon<br>"
    "Project AHAA © 2026</small>",
    unsafe_allow_html=True,
)