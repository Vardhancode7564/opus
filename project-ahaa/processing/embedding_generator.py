"""Embedding Generator - Uses SentenceTransformers to create embeddings."""

from sentence_transformers import SentenceTransformer
import logging

from config import EMBEDDING_MODEL

logger = logging.getLogger(__name__)

# Singleton model instance
_model = None


def get_model():
    """Load the SentenceTransformers model (cached)."""
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def generate_embedding(text):
    """Generate embedding vector for a single text string."""
    model = get_model()
    embedding = model.encode(text, show_progress_bar=False)
    return embedding.tolist()


def generate_embeddings_batch(texts):
    """Generate embeddings for a batch of text strings."""
    model = get_model()
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    return [emb.tolist() for emb in embeddings]
