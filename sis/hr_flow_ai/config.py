"""
HR-Flow AI — Configuration Management
=======================================
Centralised configuration loader. All settings are read from environment
variables (populated via a .env file in development) and exposed as
typed, validated attributes on a frozen dataclass.

Usage:
    from config import settings
    print(settings.BOT_TOKEN)
"""

from __future__ import annotations

import os
import logging
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load .env from the project root (same directory as this file)
# ---------------------------------------------------------------------------
_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)


def _require_env(key: str) -> str:
    """Return the value of an environment variable or raise early."""
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Required environment variable '{key}' is missing or empty. "
            f"Check your .env file at {_ENV_PATH}"
        )
    return value


# ---------------------------------------------------------------------------
# Settings dataclass
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Settings:
    """Immutable application-wide settings."""

    # Telegram
    BOT_TOKEN: str
    ADMIN_ID: int  # Telegram user ID allowed to run /admin_stats

    # AI Provider (Google Gemini)
    AI_API_KEY: str
    AI_MODEL: str

    # Database
    DATABASE_PATH: Path

    # Logging
    LOG_LEVEL: str

    # FinOps
    COST_PER_MILLION_TOKENS: float  # USD, for virtual cost estimates


def _load_settings() -> Settings:
    """Build a Settings instance from the current environment."""
    return Settings(
        BOT_TOKEN=_require_env("BOT_TOKEN"),
        ADMIN_ID=int(os.getenv("ADMIN_ID", "0")),
        AI_API_KEY=_require_env("AI_API_KEY"),
        AI_MODEL=os.getenv("AI_MODEL", "gemini-1.5-flash"),
        DATABASE_PATH=Path(os.getenv("DATABASE_PATH", "database/hr_flow.db")),
        LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
        COST_PER_MILLION_TOKENS=float(
            os.getenv("COST_PER_MILLION_TOKENS", "0.075")
        ),
    )


# Singleton — import `settings` anywhere in the project.
settings = _load_settings()


# ---------------------------------------------------------------------------
# Logging bootstrap
# ---------------------------------------------------------------------------
def configure_logging() -> None:
    """Set up root logger based on settings.LOG_LEVEL."""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
