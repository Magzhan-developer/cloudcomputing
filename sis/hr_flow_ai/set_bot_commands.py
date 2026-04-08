"""
Set Bot Commands — Telegram menu registration
================================================
Registers the bot's command list with Telegram so users see
a command menu when they type ``/`` in the chat.

Usage:
    python set_bot_commands.py

This script is idempotent — safe to run multiple times.
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from aiogram import Bot
from aiogram.types import BotCommand

# ───────────────────── load .env ────────────────────────────────────────

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
if not BOT_TOKEN:
    print("❌ BOT_TOKEN is not set in .env — aborting.")
    sys.exit(1)

# ───────────────────── command list ─────────────────────────────────────

COMMANDS = [
    BotCommand(command="start",       description="🚀 Launch the bot & Welcome message"),
    BotCommand(command="vacancies",   description="🏢 View open vacancies"),
    BotCommand(command="upload",      description="📄 Upload a resume (PDF/TXT)"),
    BotCommand(command="admin_stats", description="📊 FinOps Dashboard (Admin only)"),
]

# ───────────────────── main ─────────────────────────────────────────────


async def main() -> None:
    """Register bot commands with Telegram."""
    bot = Bot(token=BOT_TOKEN)

    print("┌──────────────────────────────────────────────┐")
    print("│  HR-Flow AI — Set Bot Commands               │")
    print("└──────────────────────────────────────────────┘")
    print()

    try:
        await bot.set_my_commands(COMMANDS)
        print("✅ Commands registered successfully!\n")
        print("   Users will now see this menu when they type /:\n")
        for cmd in COMMANDS:
            print(f"   /{cmd.command:<14} — {cmd.description}")
        print()

        # Verify by reading back
        registered = await bot.get_my_commands()
        print(f"   📋 Verified: {len(registered)} command(s) active on Telegram.")

    except Exception as exc:
        print(f"❌ Failed to set commands: {exc}")
        sys.exit(1)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
