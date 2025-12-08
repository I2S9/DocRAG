"""Test script for embedding and FAISS indexing."""

import sys
from pathlib import Path

import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.embed.embedding_model import EmbeddingModel
from src.embed.faiss_index import FAISSIndex
from src.parse.chunker import chunk_text
from src.parse.pdf_parser import extract_text_from_pdf
from src.parse.text_cleaner import clean_text


def test_embedding_and_search() -> None:
    """Test embedding and FAISS search with a PDF document."""
    docs_dir = Path("docs")

    # Look for PDF files in docs directory
    pdf_files = list(docs_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in docs/ directory.")
        print("Please add a PDF file to docs/ to test embedding and search.")
        return

    # Use the first PDF found
    pdf_path = pdf_files[0]
    print(f"Testing with: {pdf_path}")

    try:
        # Step 1: Parse PDF
        print("\n[1/4] Parsing PDF...")
        raw_text = extract_text_from_pdf(str(pdf_path))
        cleaned_text = clean_text(raw_text)
        print(f"Extracted {len(cleaned_text)} characters")

        # Step 2: Chunk text
        print("\n[2/4] Chunking text...")
        chunks = chunk_text(cleaned_text, max_tokens=300, overlap=50)
        print(f"Created {len(chunks)} chunks")

        # Step 3: Initialize embedding model and FAISS index
        print("\n[3/4] Initializing embedding model and FAISS index...")
        embedding_model = EmbeddingModel()
        embeddings = embedding_model.embed(chunks)
        print(f"Generated embeddings of shape: {embeddings.shape}")

        # Create FAISS index
        dimension = embeddings.shape[1]
        index = FAISSIndex(dimension)
        index.add(embeddings, chunks)
        print(f"Added {len(chunks)} vectors to FAISS index")

        # Step 4: Test search
        print("\n[4/4] Testing search...")
        query = "technical documentation"
        print(f"Query: '{query}'")
        query_embedding = embedding_model.embed([query])
        results = index.search(query_embedding, k=3)

        print("\n" + "=" * 80)
        print("Search Results:")
        print("=" * 80)
        for i, (text, distance) in enumerate(results, 1):
            print(f"\nResult {i} (distance: {distance:.4f}):")
            print("-" * 80)
            print(text[:300] + "..." if len(text) > 300 else text)
            print("-" * 80)

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_embedding_and_search()

