"""
Handler — Resume upload & analysis
=====================================
Accepts a candidate's resume (PDF document **or** plain text) after
a vacancy has been selected, runs it through the AI screening pipeline,
persists the result, and replies with a formatted evaluation card.

Validation rules:
    • Max file size: 5 MB
    • Accepted formats: PDF (.pdf) and TXT (.txt)
    • Scanned / image-only PDFs are detected and rejected gracefully

Flow:
    /vacancies  →  tap inline button  →  FSM enters ``waiting_for_resume``
    →  user sends PDF/TXT or pastes text  →  extract  →  AI analyse  →  DB save  →  reply
"""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from handlers.vacancy import ResumeFlow
from services.pdf_parser import extract_text
from services.ai_service import (
    analyze_resume,
    AIQuotaExceededError,
    AIAuthenticationError,
    AIServiceError,
)
from database.db import get_vacancy, save_application

logger = logging.getLogger(__name__)
router = Router(name="resume_handler")

# ─────────────────────── constants ──────────────────────────────────────

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "text/plain",
}


@router.message(Command("upload"))
async def upload_no_state(message: Message):
    await message.answer("Сначала выберите вакансию через /vacancies, чтобы я знал, по каким критериям оценивать ваше резюме.")


# ───────────────────── document upload (PDF / TXT) ──────────────────────


@router.message(ResumeFlow.waiting_for_resume, F.document)
async def handle_document_upload(message: Message, state: FSMContext, bot: Bot) -> None:
    """Handle a PDF or TXT resume upload while in the waiting_for_resume state."""
    document = message.document

    # ── validate file size ───────────────────────────────────────────
    if document.file_size and document.file_size > MAX_FILE_SIZE_BYTES:
        size_mb = document.file_size / (1024 * 1024)
        await message.answer(
            f"⚠️ File too large (<b>{size_mb:.1f} MB</b>).\n"
            f"Maximum allowed size is <b>5 MB</b>. "
            f"Please compress your file or paste the text directly."
        )
        return

    # ── validate mime type ───────────────────────────────────────────
    if document.mime_type not in ALLOWED_MIME_TYPES:
        await message.answer(
            "⚠️ Unsupported file format.\n"
            "Please upload a <b>PDF</b> or <b>TXT</b> file, "
            "or paste your resume as plain text."
        )
        return

    await message.answer("📄 Resume received! Extracting text …")

    # ── download to a temp file ──────────────────────────────────────
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / (document.file_name or "resume")
        await bot.download(document, destination=file_path)

        # ── extract text ─────────────────────────────────────────────
        if document.mime_type == "application/pdf":
            resume_text = await extract_text(file_path)
        else:
            # text/plain
            resume_text = file_path.read_text(encoding="utf-8", errors="replace")

    # ── handle scanned / image-only PDFs ─────────────────────────────
    if not resume_text.strip():
        await message.answer(
            "⚠️ <b>No selectable text found</b> in this file.\n\n"
            "If this is a scanned PDF (image-based), our system cannot "
            "process it yet.\n\n"
            "💡 <b>What you can do:</b>\n"
            "  1. Use an OCR tool to convert the scan to text\n"
            "  2. Paste your resume as plain text in this chat\n"
            "  3. Upload a digitally-created PDF"
        )
        return

    await _run_screening(message, state, resume_text)


# ───────────────────── plain-text resume ────────────────────────────────


@router.message(ResumeFlow.waiting_for_resume, F.text)
async def handle_text_resume(message: Message, state: FSMContext) -> None:
    """Handle a resume pasted as plain text."""
    resume_text = message.text.strip()

    if len(resume_text) < 50:
        await message.answer(
            "⚠️ That seems too short to be a resume. "
            "Please send at least a few sentences, or upload a PDF."
        )
        return

    await _run_screening(message, state, resume_text)


# ───────────────────── shared screening logic ──────────────────────────


async def _run_screening(
    message: Message,
    state: FSMContext,
    resume_text: str,
) -> None:
    """Run AI analysis, save to DB, and reply with results."""

    data = await state.get_data()
    vacancy_id: int = data["vacancy_id"]

    vacancy = await get_vacancy(vacancy_id)
    if vacancy is None:
        await message.answer("❌ Vacancy not found. Please start over with /vacancies.")
        await state.clear()
        return

    await message.answer(
        f"🤖 Analysing resume for <b>{vacancy.title}</b> — please wait …"
    )

    # ── call Gemini (with granular error handling) ────────────────────
    try:
        result = await analyze_resume(
            resume_text=resume_text,
            vacancy_requirements=vacancy.requirements_text,
        )
    except AIQuotaExceededError:
        await message.answer(
            "🚫 <b>API quota exceeded.</b>\n\n"
            "The Gemini free-tier limit has been reached.\n"
            "Please try again later or contact the administrator."
        )
        await state.clear()
        return
    except AIAuthenticationError:
        await message.answer(
            "🔑 <b>API authentication error.</b>\n\n"
            "The AI service credentials are invalid. "
            "Please contact the administrator."
        )
        await state.clear()
        return
    except AIServiceError as exc:
        logger.error("AI service error: %s", exc)
        await message.answer(
            "❌ <b>AI service error.</b>\n\n"
            f"Details: <code>{exc}</code>\n\n"
            "Please try again later."
        )
        await state.clear()
        return
    except ValueError as exc:
        logger.error("AI analysis returned invalid JSON: %s", exc)
        await message.answer(
            "❌ AI analysis returned an invalid response. Please try again."
        )
        return
    except Exception as exc:
        logger.exception("Unexpected error during AI analysis: %s", exc)
        await message.answer(
            "❌ Something went wrong with the AI service. Please try again later."
        )
        return

    # ── persist to database ──────────────────────────────────────────
    score = result.get("score", 0)
    summary = result.get("summary", "")
    pros = result.get("pros", [])
    cons = result.get("cons", [])
    tokens_used = result.get("tokens_used", 0)

    candidate_name = (
        message.from_user.full_name if message.from_user else "Unknown"
    )

    await save_application(
        vacancy_id=vacancy_id,
        candidate_name=candidate_name,
        score=score,
        summary=summary,
        tokens_used=tokens_used,
        cost=0.0,
    )

    # ── format & send result ─────────────────────────────────────────
    pros_text = "\n".join(f"  • {p}" for p in pros) if pros else "  —"
    cons_text = "\n".join(f"  • {c}" for c in cons) if cons else "  —"

    score_bar = _render_score_bar(score, max_score=10)

    reply = (
        f"{'─' * 28}\n"
        f"📊 <b>Screening Result</b>\n"
        f"{'─' * 28}\n\n"
        f"🏢 <b>Vacancy:</b> {vacancy.title}\n"
        f"👤 <b>Candidate:</b> {candidate_name}\n\n"
        f"⭐ <b>Score:</b> {score}/10\n"
        f"{score_bar}\n\n"
        f"📝 <b>Summary:</b>\n{summary}\n\n"
        f"✅ <b>Pros:</b>\n{pros_text}\n\n"
        f"⚠️ <b>Cons:</b>\n{cons_text}\n\n"
        f"{'─' * 28}\n"
        f"🔢 Tokens used: <code>{tokens_used}</code>\n"
        f"{'─' * 28}\n\n"
        f"Send another resume or pick a new vacancy with /vacancies."
    )

    await message.answer(reply)

    # ── reset FSM ────────────────────────────────────────────────────
    await state.clear()


# ───────────────────── helpers ──────────────────────────────────────────


def _render_score_bar(score: int | float, max_score: int = 10) -> str:
    """Render a visual score bar like: [████████░░] 8/10"""
    filled = int(round(float(score)))
    filled = max(0, min(filled, max_score))
    empty = max_score - filled
    return f"[{'█' * filled}{'░' * empty}]"
