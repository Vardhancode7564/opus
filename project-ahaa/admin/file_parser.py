"""File Parser - Extracts text from uploaded PDF, DOCX, and TXT files."""

import logging

logger = logging.getLogger(__name__)


def parse_file(uploaded_file):
    """
    Parse an uploaded file and extract text content.
    Supports PDF, DOCX, and TXT formats.
    Returns a dict with project_title, description, source, etc.
    """
    filename = uploaded_file.name
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    text = ""
    if ext == "pdf":
        text = _parse_pdf(uploaded_file)
    elif ext == "docx":
        text = _parse_docx(uploaded_file)
    elif ext == "txt":
        text = _parse_txt(uploaded_file)
    else:
        logger.warning(f"Unsupported file format: {ext}")
        return None

    if not text.strip():
        return None

    # Use filename (without extension) as project title
    title = filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()

    return {
        "project_title": title,
        "description": text[:1000],  # First 1000 chars as description
        "technologies": "General",
        "source": "admin",
        "project_link": f"Uploaded: {filename}",
    }


def _parse_pdf(file):
    """Extract text from a PDF file."""
    try:
        from pypdf import PdfReader

        reader = PdfReader(file)
        text_parts = []
        for page in reader.pages[:20]:  # Limit to 20 pages
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return "\n".join(text_parts)
    except Exception as e:
        logger.error(f"Error parsing PDF: {e}")
        return ""


def _parse_docx(file):
    """Extract text from a DOCX file."""
    try:
        from docx import Document

        doc = Document(file)
        text_parts = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(text_parts)
    except Exception as e:
        logger.error(f"Error parsing DOCX: {e}")
        return ""


def _parse_txt(file):
    """Extract text from a TXT file."""
    try:
        content = file.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8", errors="ignore")
        return content
    except Exception as e:
        logger.error(f"Error parsing TXT: {e}")
        return ""
