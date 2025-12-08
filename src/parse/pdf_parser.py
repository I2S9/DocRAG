"""PDF parsing module for extracting text from PDF files."""

from typing import List
from pypdf import PdfReader


def extract_text_from_pdf(path: str) -> str:
    """Extract raw text from a PDF file."""
    reader = PdfReader(path)
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n".join(pages)

