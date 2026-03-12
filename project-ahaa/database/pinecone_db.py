"""Pinecone Vector Database - Stores and queries project embeddings."""

from pinecone import Pinecone, ServerlessSpec
import hashlib
import logging
import time

from config import PINECONE_API_KEY, PINECONE_INDEX, EMBEDDING_DIMENSION

logger = logging.getLogger(__name__)

_index = None


def _get_index():
    """Get or create the Pinecone index."""
    global _index
    if _index is not None:
        return _index

    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY is not set. Please add it to your .env file.")

    pc = Pinecone(api_key=PINECONE_API_KEY)

    # If PINECONE_INDEX is a URL (host), connect directly
    if PINECONE_INDEX.startswith("https://"):
        _index = pc.Index(host=PINECONE_INDEX)
        return _index

    # Otherwise treat as index name
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    if PINECONE_INDEX not in existing_indexes:
        logger.info(f"Creating Pinecone index: {PINECONE_INDEX}")
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        # Wait for index to be ready
        time.sleep(5)

    _index = pc.Index(PINECONE_INDEX)
    return _index


def _make_id(project_title, source):
    """Generate a deterministic ID for a project."""
    raw = f"{source}:{project_title}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:32]


def upsert_project(project, embedding):
    """Store a single project embedding with metadata in Pinecone."""
    index = _get_index()
    project_id = _make_id(project["project_title"], project.get("source", "unknown"))

    metadata = {
        "project_title": project.get("project_title", "")[:200],
        "description": project.get("description", "")[:500],
        "technologies": project.get("technologies", "")[:200],
        "source": project.get("source", "unknown"),
        "project_link": project.get("project_link", "")[:500],
    }

    index.upsert(vectors=[(project_id, embedding, metadata)])
    return project_id


def upsert_projects_batch(projects, embeddings):
    """Store multiple projects in Pinecone."""
    index = _get_index()
    vectors = []

    for project, embedding in zip(projects, embeddings):
        project_id = _make_id(project["project_title"], project.get("source", "unknown"))
        metadata = {
            "project_title": project.get("project_title", "")[:200],
            "description": project.get("description", "")[:500],
            "technologies": project.get("technologies", "")[:200],
            "source": project.get("source", "unknown"),
            "project_link": project.get("project_link", "")[:500],
        }
        vectors.append((project_id, embedding, metadata))

    # Upsert in batches of 100
    for i in range(0, len(vectors), 100):
        batch = vectors[i : i + 100]
        index.upsert(vectors=batch)

    return len(vectors)


def search_similar(query_embedding, top_k=5):
    """Search for the most similar projects to the query embedding."""
    index = _get_index()
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    similar_projects = []
    for match in results.get("matches", []):
        project = match.get("metadata", {})
        project["similarity_score"] = round(match.get("score", 0), 4)
        similar_projects.append(project)

    return similar_projects


def get_all_projects(limit=200):
    """
    Fetch all stored projects from Pinecone.
    Uses a list query approach since Pinecone doesn't support 'list all'.
    We do a broad query with a zero vector to get all results.
    """
    index = _get_index()
    zero_vector = [0.0] * EMBEDDING_DIMENSION
    results = index.query(
        vector=zero_vector, top_k=limit, include_metadata=True
    )

    projects = []
    for match in results.get("matches", []):
        proj = match.get("metadata", {})
        proj["id"] = match.get("id", "")
        projects.append(proj)

    return projects


def get_index_stats():
    """Get statistics about the Pinecone index."""
    try:
        index = _get_index()
        stats = index.describe_index_stats()
        return {
            "total_vectors": stats.get("total_vector_count", 0),
            "dimension": stats.get("dimension", EMBEDDING_DIMENSION),
        }
    except Exception as e:
        logger.error(f"Error getting index stats: {e}")
        return {"total_vectors": 0, "dimension": EMBEDDING_DIMENSION}


def delete_all():
    """Delete all vectors from the index."""
    index = _get_index()
    index.delete(delete_all=True)
    logger.info("All vectors deleted from Pinecone index.")
