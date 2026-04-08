"""
Service — AI Resume Screening (Google Gemini)
================================================
Uses the **google-generativeai** SDK to evaluate candidate resumes
against vacancy requirements via the Gemini 1.5 Flash model.

Public API:
    result = await analyze_resume(resume_text, vacancy_requirements)
    # result => {
    #     "score": int,
    #     "summary": str,
    #     "pros": list[str],
    #     "cons": list[str],
    #     "tokens_used": int,
    # }

Custom exceptions:
    AIQuotaExceededError   — Gemini free-tier quota exhausted
    AIAuthenticationError  — invalid or missing API key
    AIServiceError         — any other Gemini API failure
"""

from __future__ import annotations

import json
import logging
import asyncio
from typing import Any

import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

from config import settings

logger = logging.getLogger(__name__)


# ───────────────── custom exceptions ────────────────────────────────────


class AIServiceError(Exception):
    """Base exception for AI service failures."""


class AIQuotaExceededError(AIServiceError):
    """Raised when the Gemini API quota is exhausted."""


class AIAuthenticationError(AIServiceError):
    """Raised when the API key is invalid or missing."""


# ───────────────── Gemini client initialisation ─────────────────────────

genai.configure(api_key=settings.AI_API_KEY)

_model = genai.GenerativeModel(
    model_name=settings.AI_MODEL,
    system_instruction=(
        "You are a professional HR Director for a high-end restaurant chain "
        "in Almaty, Kazakhstan. Your task is to evaluate a candidate's resume "
        "against specific vacancy requirements.\n"
        "Scale: 1-10.\n"
        "Key focus areas: Hospitality experience, language proficiency "
        "(Russian, Kazakh, English), and proximity to Almaty.\n"
        "Return ONLY a valid JSON object with these keys: "
        '"score", "summary", "pros", "cons". '
        "Do not include markdown formatting or backticks in the response."
    ),
)


# ────────────────────── public interface ────────────────────────────────


async def analyze_resume(
    resume_text: str,
    vacancy_requirements: str,
) -> dict[str, Any]:
    """
    Send a resume and vacancy requirements to Gemini and return a
    structured evaluation.

    Args:
        resume_text:           Plain-text content extracted from the PDF.
        vacancy_requirements:  The requirements_text field of a vacancy.

    Returns:
        A dict with keys:
            score        (int)       — 1-10 relevance rating
            summary      (str)       — brief evaluation narrative
            pros         (list[str]) — candidate strengths
            cons         (list[str]) — candidate weaknesses / gaps
            tokens_used  (int)       — total tokens consumed (FinOps)

    Raises:
        AIQuotaExceededError:   If the free-tier quota is exhausted.
        AIAuthenticationError:  If the API key is invalid.
        AIServiceError:         On any other Gemini API error.
        ValueError:             If the response cannot be parsed as JSON.
    """

    prompt = (
        f"=== VACANCY REQUIREMENTS ===\n{vacancy_requirements}\n\n"
        f"=== CANDIDATE RESUME ===\n{resume_text}"
    )

    logger.info("Sending resume to Gemini (%s) for analysis …", settings.AI_MODEL)

    # ── call Gemini (sync SDK → offloaded to thread) ─────────────────
    try:
        response = await asyncio.to_thread(_model.generate_content, prompt)
    except google_exceptions.ResourceExhausted as exc:
        logger.error("Gemini quota exceeded: %s", exc)
        raise AIQuotaExceededError(
            "API quota exceeded. The free-tier limit has been reached. "
            "Please try again later or upgrade your plan."
        ) from exc
    except google_exceptions.PermissionDenied as exc:
        logger.error("Gemini authentication error: %s", exc)
        raise AIAuthenticationError(
            "Invalid API key. Please check your AI_API_KEY in .env."
        ) from exc
    except google_exceptions.InvalidArgument as exc:
        logger.error("Gemini invalid argument: %s", exc)
        raise AIServiceError(
            f"Gemini rejected the request: {exc}"
        ) from exc
    except google_exceptions.GoogleAPICallError as exc:
        logger.error("Gemini API error: %s", exc)
        raise AIServiceError(
            f"Google API error: {exc}"
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected error calling Gemini: %s", exc)
        raise AIServiceError(
            f"Unexpected AI service error: {exc}"
        ) from exc

    # ── FinOps: extract token usage ──────────────────────────────────
    tokens_used: int = 0
    if hasattr(response, "usage_metadata") and response.usage_metadata:
        tokens_used = getattr(response.usage_metadata, "total_token_count", 0)
        logger.info(
            "Gemini token usage — prompt: %s, candidates: %s, total: %s",
            getattr(response.usage_metadata, "prompt_token_count", "?"),
            getattr(response.usage_metadata, "candidates_token_count", "?"),
            tokens_used,
        )

    # ── Parse the JSON response ──────────────────────────────────────
    raw_text = response.text.strip()
    logger.debug("Raw Gemini response:\n%s", raw_text)

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        # Attempt to salvage if model wrapped JSON in markdown fences
        cleaned = _strip_markdown_fences(raw_text)
        try:
            result = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse Gemini response as JSON:\n%s", raw_text)
            raise ValueError(
                "The AI model returned an unparseable response. "
                "Please try again."
            ) from exc

    # ── Normalise & enrich ───────────────────────────────────────────
    result.setdefault("score", 0)
    result.setdefault("summary", "")
    result.setdefault("pros", [])
    result.setdefault("cons", [])
    result["tokens_used"] = tokens_used

    return result


# ──────────────────────── helpers ────────────────────────────────────────


def _strip_markdown_fences(text: str) -> str:
    """Remove ```json ... ``` wrappers if the model added them."""
    lines = text.splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines)
