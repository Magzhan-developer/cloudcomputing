"""
Database — Data models / DTOs
==============================
Plain dataclasses mirroring the two core tables: vacancies and
applications.  Used as typed containers throughout the application.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Vacancy:
    """A restaurant job vacancy."""

    id: int | None = None
    title: str = ""
    description: str = ""
    requirements_text: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Application:
    """
    Result of an AI resume screening for a specific vacancy.

    Attributes:
        vacancy_id:      FK → vacancies.id
        candidate_name:  Name extracted from the resume / provided by user
        score:           AI-assigned relevance score (0–100)
        summary:         Short AI-generated evaluation summary
        tokens_used:     Total LLM tokens consumed for this screening
        cost:            Estimated API cost in USD for this screening
    """

    id: int | None = None
    vacancy_id: int = 0
    candidate_name: str = ""
    score: float = 0.0
    summary: str = ""
    tokens_used: int = 0
    cost: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
