import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
import streamlit as st

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY") or st.secrets.get("PINECONE_API_KEY", "")

PINECONE_INDEX = os.getenv("PINECONE_INDEX") or st.secrets.get("PINECONE_INDEX", "project-ahaa")

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# Similarity threshold for knowledge graph edges
SIMILARITY_THRESHOLD = 0.55

# Groq model
GROQ_MODEL = "llama-3.1-8b-instant"

# GitHub API
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_API_URL = "https://api.github.com"

# Default scraping targets
DEFAULT_WEB_SOURCES = [
    "https://github.com/topics/student-project",
]
