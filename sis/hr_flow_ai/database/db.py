"""
Database — SQLite initialisation & helpers
============================================
Async helper layer built on **aiosqlite**.  Provides:

* ``init_db()``              — creates tables on first run
* ``add_vacancy()``          — insert a new vacancy
* ``get_vacancy()``          — fetch a single vacancy by id
* ``get_all_vacancies()``    — list every vacancy
* ``save_application()``     — persist an AI screening result
* ``get_applications()``     — retrieve applications for a vacancy
* ``get_stats()``            — aggregate FinOps usage statistics
"""

from __future__ import annotations

from typing import Optional

import aiosqlite

from config import settings
from database.models import Vacancy, Application

# Resolved once at import time; stays consistent for the process lifetime.
_DB_PATH: str = str(settings.DATABASE_PATH)


# ─────────────────────────────── schema ────────────────────────────────


async def init_db() -> None:
    """Create the database file and tables if they don't already exist."""
    settings.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    async with aiosqlite.connect(_DB_PATH) as db:
        await db.executescript(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                title             TEXT    NOT NULL,
                description       TEXT    NOT NULL DEFAULT '',
                requirements_text TEXT    NOT NULL DEFAULT '',
                created_at        TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS applications (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                vacancy_id      INTEGER NOT NULL REFERENCES vacancies(id),
                candidate_name  TEXT    NOT NULL,
                score           REAL    NOT NULL DEFAULT 0,
                summary         TEXT    NOT NULL DEFAULT '',
                tokens_used     INTEGER NOT NULL DEFAULT 0,
                cost            REAL    NOT NULL DEFAULT 0,
                created_at      TEXT    DEFAULT (datetime('now'))
            );
            """
        )
        await db.commit()


# ──────────────────────────── vacancies ─────────────────────────────────


async def add_vacancy(
    title: str,
    description: str = "",
    requirements_text: str = "",
) -> int:
    """
    Insert a new vacancy and return its generated ``id``.

    Args:
        title:             Short job title, e.g. "Head Chef".
        description:       Free-form description of the role.
        requirements_text: Bullet-point or prose requirements the AI will
                           compare resumes against.

    Returns:
        The auto-incremented row id of the new vacancy.
    """
    async with aiosqlite.connect(_DB_PATH) as db:
        cursor = await db.execute(
            """
            INSERT INTO vacancies (title, description, requirements_text)
            VALUES (?, ?, ?)
            """,
            (title, description, requirements_text),
        )
        await db.commit()
        return cursor.lastrowid  # type: ignore[return-value]


async def get_vacancy(vacancy_id: int) -> Optional[Vacancy]:
    """
    Fetch a single vacancy by its primary key.

    Returns:
        A ``Vacancy`` dataclass instance, or ``None`` if not found.
    """
    async with aiosqlite.connect(_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM vacancies WHERE id = ?", (vacancy_id,)
        )
        row = await cursor.fetchone()

    if row is None:
        return None

    return Vacancy(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        requirements_text=row["requirements_text"],
    )


async def get_all_vacancies() -> list[Vacancy]:
    """
    Return every vacancy ordered by most-recent first.
    """
    async with aiosqlite.connect(_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM vacancies ORDER BY created_at DESC"
        )
        rows = await cursor.fetchall()

    return [
        Vacancy(
            id=r["id"],
            title=r["title"],
            description=r["description"],
            requirements_text=r["requirements_text"],
        )
        for r in rows
    ]


# ─────────────────────────── applications ──────────────────────────────


async def save_application(
    vacancy_id: int,
    candidate_name: str,
    score: float,
    summary: str,
    tokens_used: int = 0,
    cost: float = 0.0,
) -> int:
    """
    Persist an AI screening result for a candidate–vacancy pair.

    Args:
        vacancy_id:     FK to the vacancy being applied for.
        candidate_name: The applicant's name (from resume or user input).
        score:          AI relevance score (0-100).
        summary:        AI-generated evaluation summary.
        tokens_used:    Total LLM tokens consumed.
        cost:           Estimated API cost (USD).

    Returns:
        The auto-incremented row id of the new application.
    """
    async with aiosqlite.connect(_DB_PATH) as db:
        cursor = await db.execute(
            """
            INSERT INTO applications
                (vacancy_id, candidate_name, score, summary, tokens_used, cost)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (vacancy_id, candidate_name, score, summary, tokens_used, cost),
        )
        await db.commit()
        return cursor.lastrowid  # type: ignore[return-value]


async def get_applications(vacancy_id: int) -> list[Application]:
    """
    Retrieve all screening results for a given vacancy, ordered
    by score descending (best candidates first).

    Args:
        vacancy_id: The vacancy to filter by.

    Returns:
        A list of ``Application`` dataclass instances.
    """
    async with aiosqlite.connect(_DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            """
            SELECT * FROM applications
            WHERE vacancy_id = ?
            ORDER BY score DESC
            """,
            (vacancy_id,),
        )
        rows = await cursor.fetchall()

    return [
        Application(
            id=r["id"],
            vacancy_id=r["vacancy_id"],
            candidate_name=r["candidate_name"],
            score=r["score"],
            summary=r["summary"],
            tokens_used=r["tokens_used"],
            cost=r["cost"],
        )
        for r in rows
    ]


# ──────────────────────── FinOps stats ─────────────────────────────────


async def get_stats() -> dict:
    """
    Aggregate usage statistics across all screenings.

    Returns:
        A dict with keys:
            total_screenings  (int)   — number of applications
            total_tokens      (int)   — sum of tokens_used
            total_cost        (float) — sum of cost column
            avg_score         (float) — average AI score
    """
    async with aiosqlite.connect(_DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT
                COUNT(*)           AS total_screenings,
                COALESCE(SUM(tokens_used), 0) AS total_tokens,
                COALESCE(SUM(cost), 0)        AS total_cost,
                COALESCE(AVG(score), 0)       AS avg_score
            FROM applications
            """
        )
        row = await cursor.fetchone()

    return {
        "total_screenings": row[0],
        "total_tokens": row[1],
        "total_cost": row[2],
        "avg_score": round(row[3], 2),
    }

