"""Test script for PDF parsing functionality."""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.parse.pdf_parser import extract_text_from_pdf
from src.parse.text_cleaner import clean_text


def test_pdf_parsing() -> None:
    """Test PDF parsing with an example file."""
    docs_dir = Path("docs")
    
    # Look for PDF files in docs directory
    pdf_files = list(docs_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in docs/ directory.")
        print("Please add a PDF file to docs/ to test parsing.")
        return
    
    # Use the first PDF found
    pdf_path = pdf_files[0]
    print(f"Testing with: {pdf_path}")
    
    try:
        # Extract raw text
        raw_text = extract_text_from_pdf(str(pdf_path))
        
        # Clean the text
        cleaned_text = clean_text(raw_text)
        
        # Display first 500 characters
        print("\n" + "=" * 80)
        print("First 500 characters of extracted text:")
        print("=" * 80)
        print(cleaned_text[:500])
        print("=" * 80)
        print(f"\nTotal length: {len(cleaned_text)} characters")
        
    except Exception as e:
        print(f"Error parsing PDF: {e}")


if __name__ == "__main__":
    test_pdf_parsing()

