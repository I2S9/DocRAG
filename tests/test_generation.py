"""Test script for LLM generation with RAG."""

import subprocess
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.embed.embedding_model import EmbeddingModel
from src.embed.vector_store import FaissVectorStore
from src.generation.llm_client import OllamaClient
from src.generation.prompt_builder import build_technical_doc_prompt
from src.parse.chunker import chunk_text
from src.parse.pdf_parser import extract_text_from_pdf
from src.parse.text_cleaner import clean_text
from src.retrieval.retriever import Retriever


def test_generation() -> None:
    """Test LLM generation with RAG pipeline."""
    docs_dir = Path("docs")

    # Look for PDF files in docs directory
    pdf_files = list(docs_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in docs/ directory.")
        print("Please add a PDF file to docs/ to test generation.")
        return

    # Use the first PDF found
    pdf_path = pdf_files[0]
    print(f"Testing with: {pdf_path}")

    try:
        # Step 1: Parse and chunk document
        print("\n[1/5] Parsing and chunking document...")
        raw_text = extract_text_from_pdf(str(pdf_path))
        cleaned_text = clean_text(raw_text)
        chunks = chunk_text(cleaned_text, max_tokens=300, overlap=50)
        print(f"Created {len(chunks)} chunks")

        # Step 2: Initialize embedding model and vector store
        print("\n[2/5] Initializing embedding model and vector store...")
        embed_model = EmbeddingModel()
        embeddings = embed_model.embed(chunks)
        dimension = embeddings.shape[1]
        store = FaissVectorStore(dimension)
        store.add(embeddings, chunks)
        print(f"Indexed {len(chunks)} chunks")

        # Step 3: Create retriever and retrieve relevant contexts
        print("\n[3/5] Retrieving relevant contexts...")
        retriever = Retriever(embed_model, store)
        query = "Generate a technical specification for X"
        print(f"Query: '{query}'")
        contexts = retriever.retrieve(query, k=5)
        print(f"Retrieved {len(contexts)} relevant chunks")

        # Step 4: Build prompt
        print("\n[4/5] Building structured prompt...")
        prompt = build_technical_doc_prompt(query, contexts)
        print("Prompt built successfully")

        # Step 5: Generate with LLM
        print("\n[5/5] Generating document with LLM...")
        llm_client = OllamaClient()
        generated_text = llm_client.generate(prompt)

        print("\n" + "=" * 80)
        print("Generated Technical Document:")
        print("=" * 80)
        print(generated_text)
        print("=" * 80)

    except FileNotFoundError:
        print("\nError: Ollama not found. Please install Ollama and ensure it's in your PATH.")
        print("Visit https://ollama.ai/ for installation instructions.")
    except subprocess.CalledProcessError as e:
        print(f"\nError calling Ollama: {e}")
        print(f"Stderr: {e.stderr.decode('utf-8') if e.stderr else 'No error message'}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_generation()

