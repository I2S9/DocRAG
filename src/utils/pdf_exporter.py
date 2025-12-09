"""PDF export utilities for documents and reports."""

from io import BytesIO
from typing import Dict, Any

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER


def export_document_to_pdf(text: str, title: str = "Technical Document") -> BytesIO:
    """Convert a text document to PDF format."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=16,
        textColor="black",
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=14,
        textColor="black",
        spaceAfter=12,
        spaceBefore=12,
    )
    normal_style = ParagraphStyle(
        "CustomNormal",
        parent=styles["Normal"],
        fontSize=11,
        textColor="black",
        spaceAfter=12,
        alignment=TA_LEFT,
    )
    
    story = []
    
    # Add title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Process text line by line
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 0.1 * inch))
            continue
        
        # Check if line looks like a heading (all caps, short, or ends with colon)
        if (
            line.isupper()
            and len(line) < 100
            or line.endswith(":")
            and len(line) < 100
        ):
            story.append(Paragraph(line, heading_style))
        else:
            story.append(Paragraph(line, normal_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def export_validation_report_to_pdf(validation: Dict[str, Any], document_title: str = "Validation Report") -> BytesIO:
    """Export validation report to PDF format."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontSize=16,
        textColor="black",
        spaceAfter=30,
        alignment=TA_CENTER,
    )
    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=14,
        textColor="black",
        spaceAfter=12,
        spaceBefore=12,
    )
    normal_style = ParagraphStyle(
        "ReportNormal",
        parent=styles["Normal"],
        fontSize=11,
        textColor="black",
        spaceAfter=12,
    )
    status_style = ParagraphStyle(
        "StatusStyle",
        parent=styles["Normal"],
        fontSize=11,
        textColor="black",
        spaceAfter=8,
        leftIndent=20,
    )
    
    story = []
    
    # Add title
    story.append(Paragraph(document_title, title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Overall status
    all_present = validation.get("all_sections_present", False)
    status_text = "All required sections are present" if all_present else "Some required sections are missing"
    status_color = "green" if all_present else "orange"
    
    story.append(Paragraph(f"<b>Overall Status:</b> <font color='{status_color}'>{status_text}</font>", heading_style))
    story.append(Spacer(1, 0.1 * inch))
    
    # Section details
    story.append(Paragraph("<b>Section Status:</b>", heading_style))
    sections = validation.get("sections", {})
    
    for section, present in sections.items():
        status_text = "[OK] Present" if present else "[MISSING] Missing"
        status_color = "green" if present else "red"
        story.append(
            Paragraph(
                f"<b>{section}:</b> <font color='{status_color}'>{status_text}</font>",
                status_style,
            )
        )
    
    doc.build(story)
    buffer.seek(0)
    return buffer

