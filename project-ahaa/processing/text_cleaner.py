"""Text Cleaner - Preprocesses text data using NLTK."""

import re
import string
import nltk

# Download required NLTK data (done once)
_NLTK_DATA_DOWNLOADED = False


def _ensure_nltk_data():
    global _NLTK_DATA_DOWNLOADED
    if not _NLTK_DATA_DOWNLOADED:
        for resource in ["punkt", "punkt_tab", "stopwords"]:
            try:
                nltk.data.find(f"tokenizers/{resource}" if "punkt" in resource else f"corpora/{resource}")
            except LookupError:
                nltk.download(resource, quiet=True)
        _NLTK_DATA_DOWNLOADED = True


def clean_text(text):
    """
    Clean and preprocess text:
    - lowercase
    - remove URLs
    - remove punctuation
    - remove stopwords
    - tokenize and rejoin
    """
    if not text or not isinstance(text, str):
        return ""

    _ensure_nltk_data()
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize

    stop_words = set(stopwords.words("english"))

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Remove special characters and digits (keep letters and spaces)
    text = re.sub(r"[^a-z\s]", " ", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords and short tokens
    tokens = [t for t in tokens if t not in stop_words and len(t) > 2]

    return " ".join(tokens)


def prepare_project_text(project):
    """
    Combine project title and description into a single text for embedding.
    Uses raw text (not cleaned) for embedding - the model handles it better.
    Cleaned text is optional for other uses.
    """
    parts = []
    title = project.get("project_title", "")
    desc = project.get("description", "")
    tech = project.get("technologies", "")
    readme = project.get("readme", "")

    if title:
        parts.append(title)
    if desc:
        parts.append(desc)
    if tech and tech != "Unknown" and tech != "General":
        parts.append(f"Technologies: {tech}")
    if readme:
        # Only use the first 500 chars of README
        parts.append(readme[:500])

    return " ".join(parts)
