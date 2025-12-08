"""Embedding model for converting text to vectors."""

from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """Wrapper for sentence-transformers embedding model."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize the embedding model."""
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> np.ndarray:
        """Compute embeddings for a list of texts."""
        return np.array(self.model.encode(texts, show_progress_bar=False))

