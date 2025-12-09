"""RAG retriever module for querying document chunks."""

from typing import List

import numpy as np

from src.embed.embedding_model import EmbeddingModel
from src.embed.vector_store import FaissVectorStore


class Retriever:
    """Retriever for finding relevant document chunks."""

    def __init__(self, embed_model: EmbeddingModel, store: FaissVectorStore):
        """Initialize retriever with embedding model and vector store."""
        self.embed_model = embed_model
        self.store = store

    def retrieve(self, query: str, k: int = 5) -> List[str]:
        """Retrieve top-k relevant chunks for a query."""
        query_emb = self.embed_model.embed([query])
        results = self.store.search(query_emb, k=k)
        return [text for text, _ in results]

