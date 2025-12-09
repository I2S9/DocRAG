"""Unit tests for parsing module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parse.chunker import chunk_text
from src.parse.text_cleaner import clean_text


def test_clean_text() -> None:
    """Test text cleaning functionality."""
    dirty_text = "This   is   a    test\r\nwith\n\n\nmultiple\n\nlines\t\tand\tspaces."
    cleaned = clean_text(dirty_text)
    assert "\r" not in cleaned
    assert "\n\n\n" not in cleaned
    assert "   " not in cleaned
    assert "\t\t" not in cleaned
    assert cleaned.startswith("This")
    assert cleaned.endswith("spaces.")


def test_chunk_text() -> None:
    """Test text chunking functionality."""
    text = " ".join([f"word{i}" for i in range(1000)])
    chunks = chunk_text(text, max_tokens=100, overlap=20)
    
    assert len(chunks) > 0
    assert all(len(chunk.split()) <= 100 for chunk in chunks)
    
    # Check overlap
    if len(chunks) > 1:
        first_chunk_words = chunks[0].split()
        second_chunk_words = chunks[1].split()
        # There should be some overlap
        assert len(set(first_chunk_words) & set(second_chunk_words)) > 0


def test_chunk_text_empty() -> None:
    """Test chunking with empty text."""
    chunks = chunk_text("", max_tokens=100, overlap=20)
    assert len(chunks) == 0


def test_chunk_text_short() -> None:
    """Test chunking with text shorter than max_tokens."""
    text = "This is a short text."
    chunks = chunk_text(text, max_tokens=100, overlap=20)
    assert len(chunks) == 1
    assert chunks[0] == text

