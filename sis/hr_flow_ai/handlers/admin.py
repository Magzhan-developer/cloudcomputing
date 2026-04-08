"""
Handler — /admin_stats (FinOps dashboard)
==========================================
Restricted to ``ADMIN_ID`` from config.  Displays aggregate usage
statistics and a virtual cost estimate for Gemini token consumption.
"""

from __future__ import annotations

import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import settings
from database.db import get_stats

logger = logging.getLogger(__name__)
router = Router(name="admin")


@router.message(Command("admin_stats"))
async def cmd_admin_stats(message: Message) -> None:
    """Show FinOps statistics — admin only."""

    # ── access control ───────────────────────────────────────────────
    user_id = message.from_user.id if message.from_user else 0

    if settings.ADMIN_ID == 0:
        await message.answer(
            "⚠️ Admin access is not configured.\n"
            "Set <code>ADMIN_ID</code> in your .env file."
        )
        return

    if user_id != settings.ADMIN_ID:
        logger.warning(
            "Unauthorised /admin_stats attempt by user %s (%s)",
            user_id,
            message.from_user.full_name if message.from_user else "?",
        )
        await message.answer("🔒 Access denied. This command is restricted to admins.")
        return

    # ── fetch stats ──────────────────────────────────────────────────
    stats = await get_stats()

    total_screenings = stats["total_screenings"]
    total_tokens = stats["total_tokens"]
    total_cost = stats["total_cost"]
    avg_score = stats["avg_score"]

    # ── virtual cost estimate ────────────────────────────────────────
    # Gemini free tier has no real cost, but we project future spend
    # at the configured rate (default: $0.075 per 1M tokens).
    rate = settings.COST_PER_MILLION_TOKENS
    virtual_cost = (total_tokens / 1_000_000) * rate

    # ── format response ──────────────────────────────────────────────
    reply = (
        f"{'─' * 32}\n"
        f"📊 <b>HR-Flow AI — Admin Dashboard</b>\n"
        f"{'─' * 32}\n\n"
        f"📋 <b>Total Screenings:</b>  {total_screenings}\n"
        f"⭐ <b>Average Score:</b>     {avg_score}/10\n\n"
        f"{'─' * 32}\n"
        f"💰 <b>FinOps — Token Usage</b>\n"
        f"{'─' * 32}\n\n"
        f"🔢 <b>Total Tokens:</b>      <code>{total_tokens:,}</code>\n"
        f"💵 <b>DB Recorded Cost:</b>   ${total_cost:.4f}\n"
        f"📈 <b>Virtual Cost Est.:</b>  ${virtual_cost:.4f}\n"
        f"   <i>(at ${rate}/1M tokens)</i>\n\n"
        f"{'─' * 32}\n"
        f"ℹ️ <i>Currently on Gemini free tier.\n"
        f"Virtual cost shown for capacity planning.</i>\n"
        f"{'─' * 32}"
    )

    await message.answer(reply)
