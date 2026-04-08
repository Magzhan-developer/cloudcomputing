"""
Handler — /start command
=========================
Greets the user and presents the main menu.
"""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Welcome message and main-menu prompt."""
    await message.answer(
        "👋 <b>Welcome to HR-Flow AI!</b>\n\n"
        "I help restaurant managers screen resumes quickly using AI.\n\n"
        "Choose an action:\n"
        "• /vacancies — View open vacancies\n"
        "• /upload — Upload a resume (PDF)\n"
        "• /admin_stats — 📊 FinOps dashboard (admin only)",
    )
