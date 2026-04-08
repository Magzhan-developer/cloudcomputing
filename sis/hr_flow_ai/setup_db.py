"""
Database Setup — Initialisation + Seed Data
=============================================
Creates the SQLite database, tables, and seeds the vacancies table
with realistic test data for a restaurant chain in Almaty, Kazakhstan.

Usage:
    python setup_db.py

Behaviour:
    1. Calls ``init_db()`` to create tables (idempotent).
    2. Checks if the ``vacancies`` table is empty.
    3. If empty, inserts 5 high-quality test vacancies with detailed
       requirements including language skills (Kazakh, Russian, English).
    4. Logs all progress to the console.
"""

from __future__ import annotations

import asyncio
import logging
import sys

from database.db import init_db, add_vacancy, get_all_vacancies

# ───────────────────── logging setup ────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("setup_db")


# ───────────────────── seed data ────────────────────────────────────────

SEED_VACANCIES = [
    {
        "title": "Head Chef",
        "description": (
            "Lead the kitchen of our flagship fine-dining restaurant in Almaty. "
            "Responsible for menu development, kitchen staff management, "
            "food safety standards, and maintaining Michelin-level quality."
        ),
        "requirements_text": (
            "• 7+ years of professional kitchen experience, including 3+ years "
            "as Head Chef or Executive Chef\n"
            "• Expertise in European and Central Asian cuisine\n"
            "• Experience managing a team of 10+ kitchen staff\n"
            "• Strong knowledge of HACCP and food safety regulations in Kazakhstan\n"
            "• Ability to design seasonal menus and control food cost within 28–32%\n"
            "• Languages: fluent Russian (обязательно), conversational Kazakh "
            "(қазақ тілі — preferred), basic English (for international suppliers)\n"
            "• Culinary degree or equivalent professional certification\n"
            "• Must be based in or willing to relocate to Almaty"
        ),
    },
    {
        "title": "Waiter / Waitress",
        "description": (
            "Front-of-house service for a premium restaurant in the Esentai area. "
            "You will be the primary point of contact for guests, ensuring an "
            "exceptional dining experience from greeting to farewell."
        ),
        "requirements_text": (
            "• 1+ year of experience in full-service dining (fine dining preferred)\n"
            "• Excellent knowledge of food and beverage service etiquette\n"
            "• Ability to memorize the full menu including ingredients and allergens\n"
            "• Confident upselling skills (wine pairing, dessert recommendations)\n"
            "• Languages: fluent Russian and Kazakh (обязательно), "
            "intermediate English (B1+ for international guests)\n"
            "• Neat personal presentation, punctuality, and stress resistance\n"
            "• Flexible schedule including evenings, weekends, and holidays\n"
            "• Located in Almaty or within commuting distance"
        ),
    },
    {
        "title": "Restaurant Manager",
        "description": (
            "Oversee daily operations of a 120-seat restaurant in Almaty. "
            "Manage front-of-house and back-of-house coordination, financial "
            "reporting, staff scheduling, and guest satisfaction."
        ),
        "requirements_text": (
            "• 5+ years of experience in restaurant or hospitality management\n"
            "• Proven track record of achieving revenue targets and cost control\n"
            "• Experience with POS systems (R-Keeper, iiko, or Poster)\n"
            "• Strong leadership skills — ability to manage a team of 25+ employees\n"
            "• Knowledge of Kazakhstan labor law and sanitary regulations (СанПиН)\n"
            "• Proficiency with inventory management and supplier negotiations\n"
            "• Languages: fluent Russian and Kazakh (обязательно), "
            "upper-intermediate English (B2+ for corporate reporting)\n"
            "• Higher education in Hospitality Management, Business, or related field\n"
            "• Almaty residency required"
        ),
    },
    {
        "title": "Barista",
        "description": (
            "Join our specialty coffee bar inside a premium restaurant in Almaty. "
            "You will craft espresso-based drinks, signature cocktails, and "
            "maintain the coffee program's quality standards."
        ),
        "requirements_text": (
            "• 1+ year of barista experience in a specialty coffee shop or restaurant\n"
            "• Knowledge of espresso extraction, milk texturing, and latte art\n"
            "• Familiarity with brewing methods (V60, Chemex, AeroPress)\n"
            "• Understanding of coffee origins, roast profiles, and cupping\n"
            "• Experience with coffee equipment maintenance (grinder calibration, etc.)\n"
            "• Languages: fluent Russian (обязательно), conversational Kazakh "
            "(preferred), basic English (for menu items and international guests)\n"
            "• Food safety and hygiene certification (or willingness to obtain)\n"
            "• Energetic, detail-oriented, and friendly demeanor\n"
            "• Available for morning and afternoon shifts in Almaty"
        ),
    },
    {
        "title": "Hostess",
        "description": (
            "Be the welcoming face of our upscale restaurant in Almaty. "
            "Manage reservations, coordinate seating, handle guest inquiries, "
            "and ensure smooth front-door operations during service."
        ),
        "requirements_text": (
            "• 1+ year of experience as a hostess, receptionist, or in a "
            "customer-facing hospitality role\n"
            "• Excellent communication and interpersonal skills\n"
            "• Experience with reservation systems (e.g., BookingTable, RestoPlace)\n"
            "• Strong organizational skills — ability to manage waitlists and "
            "table turnover during peak hours\n"
            "• Professional appearance and confident demeanor\n"
            "• Languages: fluent Russian and Kazakh (обязательно), "
            "intermediate English (B1+ for international guests and tourists)\n"
            "• Knowledge of Almaty's dining scene is a plus\n"
            "• Flexible schedule including evenings and weekends\n"
            "• Must be based in Almaty"
        ),
    },
]


# ───────────────────── main logic ───────────────────────────────────────


async def main() -> None:
    """Initialise the database and seed test vacancies if needed."""

    # ── Step 1: Create tables ────────────────────────────────────────
    logger.info("🗄️  Initialising HR-Flow AI database …")
    try:
        await init_db()
    except Exception as exc:
        logger.error("❌ Database initialisation failed: %s", exc)
        sys.exit(1)
    logger.info("✅ Database ready. Tables: vacancies, applications")

    # ── Step 2: Check if seeding is needed ───────────────────────────
    existing = await get_all_vacancies()

    if existing:
        logger.info(
            "📋 Vacancies table already has %d record(s) — skipping seed.",
            len(existing),
        )
        return

    # ── Step 3: Seed vacancies ───────────────────────────────────────
    logger.info("🌱 Vacancies table is empty — seeding test data …")

    for i, vacancy in enumerate(SEED_VACANCIES, start=1):
        vacancy_id = await add_vacancy(
            title=vacancy["title"],
            description=vacancy["description"],
            requirements_text=vacancy["requirements_text"],
        )
        logger.info(
            "   [%d/%d] ✅ Inserted: %-22s (id=%d)",
            i,
            len(SEED_VACANCIES),
            vacancy["title"],
            vacancy_id,
        )

    logger.info(
        "🎉 Seeding complete — %d vacancies inserted.", len(SEED_VACANCIES)
    )


if __name__ == "__main__":
    asyncio.run(main())
