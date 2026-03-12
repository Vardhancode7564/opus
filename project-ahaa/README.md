# 🎓 Project AHAA — AI Hub for Academic Advancement

A platform that helps students discover existing project ideas so they don't repeat previous work. The system collects project data from GitHub, web sources, and admin-uploaded documents. When a student enters a project idea, the system finds similar projects and suggests improvements.

---

## Features

- **GitHub Project Collector** — Fetches student project repositories via GitHub API
- **Web Scraper** — Scrapes project ideas from web pages
- **Admin Upload** — Upload PDF, DOCX, TXT project reports
- **Semantic Similarity Search** — AI-powered search using SentenceTransformers embeddings
- **AI Suggestions** — Groq LLM generates improvement ideas
- **Knowledge Graph** — Interactive project relationship visualization

## Tech Stack

| Component       | Technology                              |
| --------------- | --------------------------------------- |
| Frontend        | Streamlit                               |
| Embeddings      | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector DB       | Pinecone                                |
| LLM             | Groq API (Llama 3.1 8B)                 |
| Scraping        | Requests + BeautifulSoup                |
| File Processing | PyPDF + python-docx                     |
| Text Processing | NLTK                                    |
| Visualization   | NetworkX + Pyvis                        |

---

## Setup Instructions

### 1. Clone / Navigate to the project

```bash
cd project-ahaa
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK data (happens automatically on first run, or manually):

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
```

### 5. Configure environment variables

Edit the `.env` file and add your API keys:

```
GROQ_API_KEY=your_groq_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX=project-ahaa
```

**Get API keys:**

- **Pinecone**: Sign up at [pinecone.io](https://www.pinecone.io/) (free tier available)
- **Groq**: Sign up at [console.groq.com](https://console.groq.com/) (free tier available)

### 6. Run the application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## Usage Guide

### Home Page

Overview of the platform and current database status.

### Submit Project Idea

1. Enter your project title and description
2. Select a domain
3. Click "Find Similar Projects"
4. View similar projects with similarity scores
5. Read AI-generated improvement suggestions

### Explore Projects

Browse all indexed projects with filters by source (GitHub, Web, Admin).

### Knowledge Graph

Interactive graph showing relationships between projects. Adjust the similarity threshold to control which connections are shown.

### Admin Panel

- **Upload Files** — Upload PDF/DOCX/TXT project reports
- **GitHub Scraper** — Fetch repositories by search query
- **Web Scraper** — Scrape project ideas from any URL
- **Database** — View stats and manage stored data

---

## Project Structure

```
project-ahaa/
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration and environment variables
├── requirements.txt                # Python dependencies
├── .env                            # API keys (not committed)
├── README.md
├── data_sources/
│   ├── github_scraper.py           # GitHub API integration
│   └── web_scraper.py              # Web page scraping
├── processing/
│   ├── text_cleaner.py             # Text preprocessing with NLTK
│   └── embedding_generator.py      # SentenceTransformers embeddings
├── database/
│   └── pinecone_db.py              # Pinecone vector database operations
├── ai_engine/
│   └── suggestion_generator.py     # Groq LLM suggestion generation
├── visualization/
│   └── graph_builder.py            # NetworkX + Pyvis knowledge graph
└── admin/
    └── file_parser.py              # PDF/DOCX/TXT file parsing
```

---

## Quick Demo Workflow

1. Start the app: `streamlit run app.py`
2. Go to **Admin Panel → GitHub Scraper**
3. Search for "student project" and fetch 15 repos
4. Go to **Submit Idea** and enter a project idea
5. See similar projects and AI suggestions
6. Check out the **Knowledge Graph**

---

Built with ❤️ for Hackathon | Project AHAA © 2026
