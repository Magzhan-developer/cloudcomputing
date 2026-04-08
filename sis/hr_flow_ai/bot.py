"""
HR-Flow AI — Application Entry Point
======================================
Bootstraps the Telegram bot (aiogram v3), registers routers / handlers,
initialises the database, and starts long-polling.

Run:
    python bot.py
"""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings, configure_logging
from handlers.start import router as start_router
from handlers.vacancy import router as vacancy_router
from handlers.resume_handler import router as resume_handler_router
from handlers.admin import router as admin_router
from database.db import init_db

logger = logging.getLogger(__name__)


async def main() -> None:
    """Entry-point coroutine."""

    # 1. Logging
    configure_logging()
    logger.info("Starting HR-Flow AI bot …")

    # 2. Database
    await init_db()
    logger.info("Database initialised.")

    # 3. Bot & Dispatcher (with FSM memory storage)
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # 4. Register handler routers (order matters for priority)
    dp.include_routers(
        start_router,
        vacancy_router,
        resume_handler_router,
        admin_router,
    )

    # 5. Start polling
    logger.info("Bot is live — polling for updates …")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot stopped gracefully.")


if __name__ == "__main__":
    asyncio.run(main())
