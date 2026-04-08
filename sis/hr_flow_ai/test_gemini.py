"""
Gemini API Diagnostic Script
==============================
Standalone connectivity test for the Google Gemini API.
Mirrors the initialisation logic from ``services/ai_service.py``
to ensure consistency.

Usage:
    python test_gemini.py

What it does:
    1. Loads AI_API_KEY from .env via python-dotenv
    2. Configures the google-generativeai SDK (same as ai_service.py)
    3. Lists all available models and checks for gemini-1.5-flash
    4. Sends a test prompt ("Hello") and prints the response
    5. Reports token usage metadata

Exit codes:
    0 — all checks passed
    1 — a specific, diagnosed error occurred
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# ───────────────────── load .env ────────────────────────────────────────

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

API_KEY = os.getenv("AI_API_KEY", "")
MODEL_NAME = os.getenv("AI_MODEL", "gemini-1.5-flash")

DIVIDER = "─" * 50


def _fail(message: str) -> None:
    """Print an error and exit with code 1."""
    print(f"\n❌ FAILED: {message}")
    sys.exit(1)


# ───────────────────── Step 0: Validate env ─────────────────────────────

print(DIVIDER)
print("🔧 Gemini API Diagnostic Tool")
print(DIVIDER)

print(f"\n📂 .env path:  {_ENV_PATH}")
print(f"🔑 AI_API_KEY: {'***' + API_KEY[-6:] if len(API_KEY) > 6 else '(not set)'}")
print(f"🤖 AI_MODEL:   {MODEL_NAME}")

if not API_KEY:
    _fail(
        "AI_API_KEY is not set.\n"
        "   → Set it in your .env file.\n"
        "   → Get a key at https://aistudio.google.com/apikey"
    )


# ───────────────────── Step 1: Configure SDK ────────────────────────────
# Same pattern as services/ai_service.py:
#   genai.configure(api_key=settings.AI_API_KEY)

import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

print("\n" + DIVIDER)
print("📡 Step 1: Configuring SDK …")
print(DIVIDER)

genai.configure(api_key=API_KEY)
print("   ✅ genai.configure() succeeded.")


# ───────────────────── Step 2: List models ──────────────────────────────

print("\n" + DIVIDER)
print("📋 Step 2: Listing available models …")
print(DIVIDER)

target_model_found = False

try:
    models = list(genai.list_models())
except google_exceptions.Unauthenticated as exc:
    _fail(
        "401 Unauthorized — Invalid API Key.\n"
        f"   → Error: {exc}\n"
        "   → Check your AI_API_KEY in .env.\n"
        "   → Regenerate at https://aistudio.google.com/apikey"
    )
except google_exceptions.PermissionDenied as exc:
    _fail(
        "403 Permission Denied.\n"
        f"   → Error: {exc}\n"
        "   → Your API key may lack the Generative Language API permission.\n"
        "   → Enable it at https://console.cloud.google.com/apis"
    )
except google_exceptions.NotFound as exc:
    _fail(
        "404 Not Found — API endpoint unreachable.\n"
        f"   → Error: {exc}\n"
        "   → The Generative Language API may not be enabled for your project."
    )
except Exception as exc:
    _fail(f"Unexpected error listing models: {type(exc).__name__}: {exc}")

generative_models = [
    m for m in models
    if "generateContent" in (m.supported_generation_methods or [])
]

print(f"\n   Found {len(generative_models)} generative model(s):\n")
for m in generative_models:
    marker = " 👈 TARGET" if MODEL_NAME in m.name else ""
    print(f"   • {m.name}{marker}")
    if MODEL_NAME in m.name:
        target_model_found = True

if not target_model_found:
    print(f"\n   ⚠️  Model '{MODEL_NAME}' was NOT found in available models.")
    print("   → Check if the model name is correct.")
    print("   → You may need a different API key or billing plan.")
else:
    print(f"\n   ✅ Target model '{MODEL_NAME}' is available.")


# ───────────────────── Step 3: Test prompt ──────────────────────────────
# Same pattern as ai_service.py:
#   _model = genai.GenerativeModel(model_name=settings.AI_MODEL, ...)

print("\n" + DIVIDER)
print("🧪 Step 3: Sending test prompt ('Hello') …")
print(DIVIDER)

model = genai.GenerativeModel(model_name=MODEL_NAME)

try:
    response = model.generate_content("Hello")
except google_exceptions.Unauthenticated as exc:
    _fail(
        "401 Unauthorized during generate_content.\n"
        f"   → Error: {exc}\n"
        "   → Your API key is invalid or has been revoked."
    )
except google_exceptions.PermissionDenied as exc:
    _fail(
        "403 Permission Denied during generate_content.\n"
        f"   → Error: {exc}\n"
        "   → API key lacks permission for this model."
    )
except google_exceptions.NotFound as exc:
    _fail(
        f"404 Not Found — Model '{MODEL_NAME}' does not exist.\n"
        f"   → Error: {exc}\n"
        "   → Try 'gemini-1.5-flash' or 'gemini-2.0-flash'.\n"
        "   → Check available models in Step 2 output above."
    )
except google_exceptions.ResourceExhausted as exc:
    _fail(
        "429 Quota Exceeded.\n"
        f"   → Error: {exc}\n"
        "   → Free-tier rate limit hit. Wait and retry.\n"
        "   → Or upgrade at https://console.cloud.google.com/billing"
    )
except google_exceptions.InvalidArgument as exc:
    _fail(
        "400 Invalid Argument.\n"
        f"   → Error: {exc}\n"
        "   → The request was malformed. Check the model name."
    )
except Exception as exc:
    _fail(f"Unexpected error: {type(exc).__name__}: {exc}")


# ───────────────────── Step 4: Print response ──────────────────────────

print(f"\n   📝 Response text:\n")
print(f"   \"{response.text.strip()}\"")

# Token usage (same logic as ai_service.py)
print(f"\n   📊 Usage metadata:")
if hasattr(response, "usage_metadata") and response.usage_metadata:
    um = response.usage_metadata
    prompt_tokens = getattr(um, "prompt_token_count", "?")
    candidate_tokens = getattr(um, "candidates_token_count", "?")
    total_tokens = getattr(um, "total_token_count", "?")
    print(f"      Prompt tokens:    {prompt_tokens}")
    print(f"      Response tokens:  {candidate_tokens}")
    print(f"      Total tokens:     {total_tokens}")
else:
    print("      (no usage metadata available)")


# ───────────────────── Summary ──────────────────────────────────────────

print("\n" + DIVIDER)
print("✅ ALL CHECKS PASSED")
print(DIVIDER)
print(f"""
   🔑 API Key:    valid
   🤖 Model:      {MODEL_NAME} — accessible
   📡 API call:   successful
   📊 Tokens:     tracked

   Your Gemini integration is ready.
   Run the bot with: python bot.py
""")
