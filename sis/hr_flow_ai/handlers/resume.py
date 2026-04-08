"""
Handler — Resume upload (DEPRECATED)
======================================
This module has been replaced by ``resume_handler.py`` which
implements PDF + plain-text support with FSM state management.

Use:
    from handlers.resume_handler import router
"""

from __future__ import annotations

from aiogram import Router

router = Router(name="resume_deprecated")
# No handlers registered — kept for reference only.
