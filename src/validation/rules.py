"""Validation rules for technical documents."""

from typing import Dict, List

REQUIRED_SECTIONS = [
    "Introduction",
    "Scope",
    "Requirements",
    "Constraints",
    "Safety considerations",
]


def check_required_sections(text: str) -> Dict[str, bool]:
    """Check presence of required sections."""
    results = {}
    for section in REQUIRED_SECTIONS:
        results[section] = section in text
    return results

