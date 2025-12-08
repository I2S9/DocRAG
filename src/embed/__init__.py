"""Embedding module for text vectorization and FAISS indexing."""

from .embedding_model import EmbeddingModel
from .faiss_index import FAISSIndex

__all__ = ["EmbeddingModel", "FAISSIndex"]

