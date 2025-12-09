"""Test script for document validation."""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.validation.validator import validate_document


def test_validation() -> None:
    """Test document validation with example documents."""
    print("Testing document validation...\n")

    # Test 1: Document with all required sections
    print("=" * 80)
    print("Test 1: Document with all required sections")
    print("=" * 80)
    complete_doc = """
    Introduction
    This document describes the technical specifications.

    Scope
    The scope covers all system components.

    Requirements
    The system must meet performance criteria.

    Constraints
    Budget and time constraints apply.

    Safety considerations
    All safety protocols must be followed.
    """
    result1 = validate_document(complete_doc)
    print(json.dumps(result1, indent=2))
    print()

    # Test 2: Document missing some sections
    print("=" * 80)
    print("Test 2: Document missing some sections")
    print("=" * 80)
    incomplete_doc = """
    Introduction
    This document describes the technical specifications.

    Scope
    The scope covers all system components.

    Requirements
    The system must meet performance criteria.
    """
    result2 = validate_document(incomplete_doc)
    print(json.dumps(result2, indent=2))
    print()

    # Test 3: Empty document
    print("=" * 80)
    print("Test 3: Empty document")
    print("=" * 80)
    empty_doc = ""
    result3 = validate_document(empty_doc)
    print(json.dumps(result3, indent=2))
    print()

    # Summary
    print("=" * 80)
    print("Validation Summary:")
    print("=" * 80)
    print(f"Test 1 (complete): {'PASS' if result1['all_sections_present'] else 'FAIL'}")
    print(f"Test 2 (incomplete): {'PASS' if not result2['all_sections_present'] else 'FAIL'}")
    print(f"Test 3 (empty): {'PASS' if not result3['all_sections_present'] else 'FAIL'}")


if __name__ == "__main__":
    test_validation()

