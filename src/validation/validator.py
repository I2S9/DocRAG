"""Document validator for checking completeness and structure."""

from typing import Any, Dict

from .rules import check_required_sections


def validate_document(text: str) -> Dict[str, Any]:
    """Run validation rules on a generated document."""
    sections_status = check_required_sections(text)
    all_present = all(sections_status.values())
    return {
        "all_sections_present": all_present,
        "sections": sections_status,
    }

