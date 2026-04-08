# 🤖 HR-Flow AI

**Automated resume screening for the restaurant industry** — powered by Google Gemini and delivered via Telegram.

HR-Flow AI helps SME restaurant managers in Almaty, Kazakhstan evaluate candidate resumes against specific vacancy requirements using AI. Results include a 1–10 score, pros/cons, and a written summary — all inside Telegram.

---

## 📁 Project Structure

```
hr_flow_ai/
├── bot.py                  # Application entry point
├── config.py               # Centralised configuration (from .env)
├── .env                    # Environment variables (secrets — not committed)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container build file
│
├── handlers/               # Telegram command & message handlers
│   ├── start.py            #   /start — welcome menu
│   ├── vacancy.py          #   /vacancies — inline keyboard selection
│   ├── resume_handler.py   #   PDF/TXT upload + AI analysis flow
│   └── admin.py            #   /admin_stats — FinOps dashboard
│
├── services/               # Core business logic
│   ├── ai_service.py       #   Gemini API integration + error handling
│   └── pdf_parser.py       #   PyMuPDF text extraction
│
└── database/               # SQLite persistence layer
    ├── db.py               #   Schema init + CRUD helpers
    └── models.py           #   Dataclass DTOs (Vacancy, Application)
```

---

## ⚡ Quick Start

### 1. Clone & install

```bash
git clone <your-repo-url>
cd hr_flow_ai
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy the `.env` template and fill in your values:

```bash
cp .env.example .env   # or edit .env directly
```

| Variable | Required | How to get it |
|---|---|---|
| `BOT_TOKEN` | ✅ | Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot` → copy the token |
| `AI_API_KEY` | ✅ | Go to [Google AI Studio](https://aistudio.google.com/apikey) → Create API Key → copy it |
| `ADMIN_ID` | ✅ | Message [@userinfobot](https://t.me/userinfobot) on Telegram → it replies with your numeric user ID |
| `AI_MODEL` | ❌ | Default: `gemini-1.5-flash`. Other options: `gemini-1.5-pro`, `gemini-2.0-flash` |
| `DATABASE_PATH` | ❌ | Default: `database/hr_flow.db`. Change if you want a custom location |
| `LOG_LEVEL` | ❌ | Default: `INFO`. Set to `DEBUG` for verbose output |
| `COST_PER_MILLION_TOKENS` | ❌ | Default: `0.075`. Virtual cost rate (USD/1M tokens) for FinOps dashboard |

**Example `.env` file:**

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
AI_API_KEY=AIzaSyD_your_gemini_key_here
AI_MODEL=gemini-1.5-flash
DATABASE_PATH=database/hr_flow.db
LOG_LEVEL=INFO
ADMIN_ID=123456789
COST_PER_MILLION_TOKENS=0.075
```

### 3. Initialize the database

The database is **auto-created** on first run — `bot.py` calls `init_db()` at startup, which:
- Creates the `database/` directory if it doesn't exist
- Creates the SQLite file (`hr_flow.db`)
- Runs `CREATE TABLE IF NOT EXISTS` for both tables

If you want to initialize the database manually **without starting the bot**:

```bash
python -c "import asyncio; from database.db import init_db; asyncio.run(init_db())"
```

### 4. Run the bot

```bash
python bot.py
```

You should see:
```
2026-04-09 02:40:00 | INFO     | __main__                  | Starting HR-Flow AI bot …
2026-04-09 02:40:00 | INFO     | __main__                  | Database initialised.
2026-04-09 02:40:00 | INFO     | __main__                  | Bot is live — polling for updates …
```

---

## 🐳 Docker

### Build

```bash
docker build -t hr-flow-ai .
```

### Run

```bash
docker run -d \
  --name hr-flow-ai \
  --env-file .env \
  -v hr-flow-data:/app/database \
  hr-flow-ai
```

> The `-v` flag mounts a named volume so the SQLite database persists across container restarts.

---

## 🗂️ Bot Commands

| Command | Access | Description |
|---|---|---|
| `/start` | Everyone | Welcome message and menu |
| `/vacancies` | Everyone | Browse open positions (inline keyboard) |
| `/admin_stats` | Admin only | FinOps dashboard — total tokens, screenings, virtual cost |

### Resume Upload Flow

1. Run `/vacancies` and tap a position
2. Send a **PDF file**, **TXT file**, or **paste text** directly
3. Receive an AI-generated screening report with score, pros, cons

**Constraints:**
- Max file size: **5 MB**
- Accepted formats: **PDF**, **TXT**, or plain text message
- Scanned (image-only) PDFs are detected and rejected with guidance

---

## 🔒 Security Notes

- **Never commit `.env`** — it's in `.gitignore`
- `ADMIN_ID` gates the `/admin_stats` command — set it to `0` to disable
- All SQL queries use parameterised placeholders to prevent injection

---

## 📊 FinOps

HR-Flow AI tracks Gemini token consumption per screening. The `/admin_stats` command shows:

- Total screenings performed
- Total tokens consumed
- Virtual cost estimate at `$COST_PER_MILLION_TOKENS` per 1M tokens

> Currently targeting Gemini's **free tier**. Virtual cost projections help plan for future scaling.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Bot framework | aiogram 3.x (async) |
| AI model | Google Gemini 1.5 Flash |
| PDF parsing | PyMuPDF (fitz) |
| Database | SQLite via aiosqlite |
| Config | python-dotenv + frozen dataclass |
| Container | Docker (python:3.10-slim) |

---

## 📜 License

This project is developed as part of the KBTU Cloud Computing course (Semester 6).
