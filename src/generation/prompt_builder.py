"""Prompt building utilities for structured document generation."""

from typing import List


def build_technical_doc_prompt(query: str, contexts: List[str]) -> str:
    """Build a structured prompt for technical document generation."""
    context_block = "\n\n".join(contexts)
    prompt = (
        "You are an assistant that generates formal technical documentation.\n"
        "Use the following context to answer.\n\n"
        "CONTEXT:\n"
        f"{context_block}\n\n"
        "TASK:\n"
        f"{query}\n\n"
        "Write a structured technical document with clear sections."
    )
    return prompt

