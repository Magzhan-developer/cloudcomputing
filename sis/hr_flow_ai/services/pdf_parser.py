"""
Service — PDF Text Extraction
===============================
Extracts plain text from uploaded PDF resumes using **PyMuPDF** (``fitz``).

The extraction runs in a thread pool to avoid blocking the asyncio
event loop on CPU-bound PDF parsing.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


async def extract_text(pdf_path: Path) -> str:
    """
    Extract all text from a PDF file.

    Args:
        pdf_path: Absolute path to the downloaded PDF.

    Returns:
        Concatenated plain-text content of all pages, separated by
        newlines.  Returns an empty string for image-only PDFs.
    """
    text = await asyncio.to_thread(_extract_sync, pdf_path)
    logger.info(
        "Extracted %d characters from %s (%d pages)",
        len(text),
        pdf_path.name,
        _page_count(pdf_path),
    )
    return text


def _extract_sync(pdf_path: Path) -> str:
    """Synchronous extraction — called inside a thread."""
    pages: list[str] = []
    with fitz.open(str(pdf_path)) as doc:
        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                pages.append(page_text.strip())
    return "\n\n".join(pages)


def _page_count(pdf_path: Path) -> int:
    """Return the number of pages without reading all text."""
    try:
        with fitz.open(str(pdf_path)) as doc:
            return len(doc)
    except Exception:
        return 0
