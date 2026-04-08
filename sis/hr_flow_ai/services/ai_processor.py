"""
Service — AI Resume Screening (DEPRECATED)
============================================
This module has been replaced by ``ai_service.py`` which uses
the Google Gemini API.  Kept temporarily for reference.

Use:
    from services.ai_service import analyze_resume
"""

from __future__ import annotations


async def screen_resume(resume_text: str, vacancy_title: str) -> dict:
    """Deprecated — use ``services.ai_service.analyze_resume`` instead."""
    raise NotImplementedError(
        "This module is deprecated. Use services.ai_service.analyze_resume()."
    )
