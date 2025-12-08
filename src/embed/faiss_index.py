"""FAISS index management for vector storage and retrieval."""

from typing import List

import numpy as np
import faiss


class FAISSIndex:
    """FAISS index wrapper for storing and searching embeddings."""

    def __init__(self, dimension: int):
        """Initialize FAISS index with given dimension."""
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []

    def add(self, embeddings: np.ndarray, texts: List[str]) -> None:
        """Add embeddings and associated texts to the index."""
        if embeddings.shape[1] != self.dimension:
            raise ValueError(
                f"Embedding dimension {embeddings.shape[1]} does not match index dimension {self.dimension}"
            )
        self.index.add(embeddings.astype("float32"))
        self.texts.extend(texts)

    def search(self, query_embedding: np.ndarray, k: int = 5) -> tuple:
        """Search for k nearest neighbors."""
        query_embedding = query_embedding.astype("float32")
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        distances, indices = self.index.search(query_embedding, k)
        results = [(self.texts[idx], float(dist)) for idx, dist in zip(indices[0], distances[0])]
        return results

    def save(self, path: str) -> None:
        """Save index to disk."""
        faiss.write_index(self.index, path)

    def load(self, path: str) -> None:
        """Load index from disk."""
        self.index = faiss.read_index(path)

