"""Knowledge Graph Builder - Creates project relationship graphs using NetworkX and Pyvis."""

import networkx as nx
from pyvis.network import Network
import os
import logging

from config import SIMILARITY_THRESHOLD

logger = logging.getLogger(__name__)


def build_knowledge_graph(projects, similarity_matrix=None):
    """
    Build a NetworkX graph from projects.
    Nodes = projects, Edges = similarity above threshold.

    If similarity_matrix is provided, use it.
    Otherwise, compute pairwise similarities using embeddings.
    """
    G = nx.Graph()

    # Add nodes
    for i, proj in enumerate(projects):
        title = proj.get("project_title", f"Project {i}")
        source = proj.get("source", "unknown")

        color_map = {
            "github": "#4078c0",
            "web": "#2ecc71",
            "admin": "#e74c3c",
        }
        color = color_map.get(source, "#95a5a6")

        G.add_node(
            title,
            label=title[:40],
            title=f"{title}\nSource: {source}\nTech: {proj.get('technologies', 'N/A')}",
            color=color,
            source=source,
            size=20,
        )

    # Add edges based on similarity
    if similarity_matrix is not None:
        for i in range(len(projects)):
            for j in range(i + 1, len(projects)):
                sim = similarity_matrix[i][j]
                if sim >= SIMILARITY_THRESHOLD:
                    title_i = projects[i].get("project_title", f"Project {i}")
                    title_j = projects[j].get("project_title", f"Project {j}")
                    G.add_edge(
                        title_i,
                        title_j,
                        weight=round(sim, 3),
                        title=f"Similarity: {sim:.3f}",
                    )

    return G


def compute_similarity_matrix(embeddings):
    """Compute pairwise cosine similarity matrix from embeddings."""
    import numpy as np

    embeddings_array = np.array(embeddings)
    # Normalize
    norms = np.linalg.norm(embeddings_array, axis=1, keepdims=True)
    norms[norms == 0] = 1  # avoid division by zero
    normalized = embeddings_array / norms
    # Cosine similarity matrix
    sim_matrix = np.dot(normalized, normalized.T)
    return sim_matrix.tolist()


def render_graph_html(G, output_path="graph.html"):
    """Render the NetworkX graph as an interactive HTML file using Pyvis."""
    net = Network(
        height="600px",
        width="100%",
        bgcolor="#1a1a2e",
        font_color="white",
        directed=False,
    )

    net.from_nx(G)

    # Physics settings for nice layout
    net.set_options("""
    {
        "physics": {
            "forceAtlas2Based": {
                "gravitationalConstant": -50,
                "centralGravity": 0.01,
                "springLength": 100,
                "springConstant": 0.08
            },
            "maxVelocity": 50,
            "solver": "forceAtlas2Based",
            "timestep": 0.35,
            "stabilization": {
                "iterations": 150
            }
        },
        "nodes": {
            "font": {
                "size": 12,
                "color": "white"
            },
            "borderWidth": 2
        },
        "edges": {
            "color": {
                "inherit": true
            },
            "smooth": false
        },
        "interaction": {
            "hover": true,
            "tooltipDelay": 200
        }
    }
    """)

    net.save_graph(output_path)
    return output_path
