"""Test script for PDF export functionality."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.pdf_exporter import export_document_to_pdf, export_validation_report_to_pdf


def test_document_export() -> None:
    """Test exporting a document to PDF."""
    print("Testing document PDF export...")
    
    sample_text = """Introduction
This document describes the technical specifications for component X.

Scope
The scope covers all system components and their interactions.

Requirements
The system must meet the following requirements:
- Performance criteria
- Safety standards
- Compliance regulations

Constraints
Budget and time constraints apply to this project.

Safety considerations
All safety protocols must be followed during implementation."""
    
    try:
        pdf_buffer = export_document_to_pdf(sample_text, "Test Document")
        print(f"PDF generated successfully. Size: {len(pdf_buffer.getvalue())} bytes")
        
        # Save to file for inspection
        output_path = Path("test_document.pdf")
        with open(output_path, "wb") as f:
            f.write(pdf_buffer.getvalue())
        print(f"PDF saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


def test_validation_report_export() -> None:
    """Test exporting a validation report to PDF."""
    print("\nTesting validation report PDF export...")
    
    validation_data = {
        "all_sections_present": True,
        "sections": {
            "Introduction": True,
            "Scope": True,
            "Requirements": True,
            "Constraints": True,
            "Safety considerations": True,
        },
    }
    
    try:
        pdf_buffer = export_validation_report_to_pdf(validation_data, "Validation Report")
        print(f"PDF generated successfully. Size: {len(pdf_buffer.getvalue())} bytes")
        
        # Save to file for inspection
        output_path = Path("test_validation_report.pdf")
        with open(output_path, "wb") as f:
            f.write(pdf_buffer.getvalue())
        print(f"PDF saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_document_export()
    test_validation_report_export()

