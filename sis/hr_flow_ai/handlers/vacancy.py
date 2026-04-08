"""
Handler — Vacancy selection (Inline Keyboard)
================================================
Lists available vacancies from the database as an inline keyboard.
When the user taps a vacancy button, the callback stores the selected
vacancy in FSM state so the resume handler knows which position the
candidate is applying for.
"""

from __future__ import annotations

import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.db import get_all_vacancies

logger = logging.getLogger(__name__)
router = Router(name="vacancy")


# ──────────────────────── FSM states ────────────────────────────────────

class ResumeFlow(StatesGroup):
    """Finite-state machine for the resume upload flow."""
    waiting_for_resume = State()


# ──────────────────────── /vacancies command ────────────────────────────


@router.message(Command("vacancies"))
async def cmd_vacancies(message: Message) -> None:
    """Show available restaurant vacancies as inline buttons."""
    vacancies = await get_all_vacancies()

    if not vacancies:
        await message.answer(
            "📭 No vacancies available right now. Check back later!"
        )
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"📌 {v.title}",
                callback_data=f"vacancy:{v.id}",
            )]
            for v in vacancies
        ]
    )

    await message.answer(
        "📋 <b>Open Vacancies</b>\n\n"
        "Tap a position below, then send your resume (PDF or plain text):",
        reply_markup=keyboard,
    )


# ──────────────────────── callback: vacancy selected ────────────────────


@router.callback_query(lambda cb: cb.data and cb.data.startswith("vacancy:"))
async def on_vacancy_selected(callback: CallbackQuery, state: FSMContext) -> None:
    """Store the chosen vacancy id in FSM and prompt for a resume."""
    vacancy_id = int(callback.data.split(":")[1])

    await state.update_data(vacancy_id=vacancy_id)
    await state.set_state(ResumeFlow.waiting_for_resume)

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        f"✅ Vacancy <b>#{vacancy_id}</b> selected.\n\n"
        "Now send your resume:\n"
        "📎 Upload a <b>PDF file</b>, or\n"
        "📝 Paste your resume as <b>plain text</b>.",
    )
    await callback.answer()
