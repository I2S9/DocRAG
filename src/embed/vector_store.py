"""Vector store interface for FAISS."""

from typing import List

import numpy as np

from src.embed.faiss_index import FAISSIndex


class FaissVectorStore:
    """Vector store wrapper around FAISS index."""

    def __init__(self, dimension: int):
        """Initialize vector store with given dimension."""
        self.index = FAISSIndex(dimension)

    def add(self, embeddings: np.ndarray, texts: List[str]) -> None:
        """Add embeddings and texts to the store."""
        self.index.add(embeddings, texts)

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[tuple]:
        """Search for k nearest neighbors."""
        return self.index.search(query_embedding, k)

    def save(self, path: str) -> None:
        """Save index to disk."""
        self.index.save(path)

    def load(self, path: str) -> None:
        """Load index from disk."""
        self.index.load(path)

