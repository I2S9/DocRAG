"""Text chunking module for splitting documents into manageable pieces."""

from typing import List


def chunk_text(text: str, max_tokens: int = 300, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks based on approximate token size."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + max_tokens
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end >= len(words):
            break
        start = end - overlap
    return chunks

