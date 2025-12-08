"""Text cleaning utilities for processing extracted text."""

import re


def clean_text(text: str) -> str:
    """Clean raw text from PDFs."""
    text = text.replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

