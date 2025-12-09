"""Test script for RAG retrieval functionality."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.embed.embedding_model import EmbeddingModel
from src.embed.vector_store import FaissVectorStore
from src.parse.chunker import chunk_text
from src.parse.pdf_parser import extract_text_from_pdf
from src.parse.text_cleaner import clean_text
from src.retrieval.retriever import Retriever


def test_retrieval() -> None:
    """Test RAG retrieval with a query."""
    docs_dir = Path("docs")

    # Look for PDF files in docs directory
    pdf_files = list(docs_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in docs/ directory.")
        print("Please add a PDF file to docs/ to test retrieval.")
        return

    # Use the first PDF found
    pdf_path = pdf_files[0]
    print(f"Testing with: {pdf_path}")

    try:
        # Step 1: Parse and chunk document
        print("\n[1/3] Parsing and chunking document...")
        raw_text = extract_text_from_pdf(str(pdf_path))
        cleaned_text = clean_text(raw_text)
        chunks = chunk_text(cleaned_text, max_tokens=300, overlap=50)
        print(f"Created {len(chunks)} chunks")

        # Step 2: Initialize embedding model and vector store
        print("\n[2/3] Initializing embedding model and vector store...")
        embed_model = EmbeddingModel()
        embeddings = embed_model.embed(chunks)
        dimension = embeddings.shape[1]
        store = FaissVectorStore(dimension)
        store.add(embeddings, chunks)
        print(f"Indexed {len(chunks)} chunks")

        # Step 3: Create retriever and test query
        print("\n[3/3] Testing retrieval...")
        retriever = Retriever(embed_model, store)

        query = "List the safety requirements for component X."
        print(f"Query: '{query}'")
        results = retriever.retrieve(query, k=5)

        print("\n" + "=" * 80)
        print("Retrieved Chunks:")
        print("=" * 80)
        for i, chunk in enumerate(results, 1):
            print(f"\nChunk {i}:")
            print("-" * 80)
            print(chunk[:400] + "..." if len(chunk) > 400 else chunk)
            print("-" * 80)

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_retrieval()

