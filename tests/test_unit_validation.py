"""Unit tests for validation module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.validation.validator import validate_document
from src.validation.rules import check_required_sections, REQUIRED_SECTIONS


def test_check_required_sections_all_present() -> None:
    """Test checking required sections when all are present."""
    text = "\n".join(REQUIRED_SECTIONS)
    result = check_required_sections(text)
    assert all(result.values())
    assert len(result) == len(REQUIRED_SECTIONS)


def test_check_required_sections_none_present() -> None:
    """Test checking required sections when none are present."""
    text = "Some random text without any required sections."
    result = check_required_sections(text)
    assert not any(result.values())


def test_check_required_sections_partial() -> None:
    """Test checking required sections when some are present."""
    text = "Introduction\nScope\nSome other text"
    result = check_required_sections(text)
    assert result["Introduction"] is True
    assert result["Scope"] is True
    assert result["Requirements"] is False
    assert result["Constraints"] is False
    assert result["Safety considerations"] is False


def test_validate_document_complete() -> None:
    """Test document validation with complete document."""
    text = "\n".join(REQUIRED_SECTIONS)
    result = validate_document(text)
    assert result["all_sections_present"] is True
    assert all(result["sections"].values())


def test_validate_document_incomplete() -> None:
    """Test document validation with incomplete document."""
    text = "Introduction\nScope"
    result = validate_document(text)
    assert result["all_sections_present"] is False
    assert result["sections"]["Introduction"] is True
    assert result["sections"]["Scope"] is True
    assert result["sections"]["Requirements"] is False


def test_validate_document_empty() -> None:
    """Test document validation with empty document."""
    result = validate_document("")
    assert result["all_sections_present"] is False
    assert not any(result["sections"].values())

