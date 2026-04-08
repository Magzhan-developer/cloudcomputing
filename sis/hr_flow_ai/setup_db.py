"""
Database Setup — Standalone initialisation script
====================================================
Run this script to create the SQLite database and tables without
starting the full bot.

Usage:
    python setup_db.py

This is equivalent to what ``bot.py`` does on startup, but useful for:
    • CI/CD pipelines — pre-create the DB before deployment
    • Docker builds — ensure the schema exists inside the image
    • Manual testing — reset/recreate the database
"""

from __future__ import annotations

import asyncio
import sys

from database.db import init_db


async def main() -> None:
    """Initialise the database and report status."""
    print("🗄️  Initialising HR-Flow AI database …")

    try:
        await init_db()
    except Exception as exc:
        print(f"❌ Database initialisation failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print("✅ Database ready.")
    print("   Tables: vacancies, applications")


if __name__ == "__main__":
    asyncio.run(main())
