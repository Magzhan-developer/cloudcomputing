# HR-Flow AI — IT4IT Value Stream & Reflective Summary

**Course:** Cloud Computing for Big Data (KBTU, Semester 6)  
**Role:** Product Architect  
**Date:** April 2026  
**Platform:** Telegram Bot (aiogram v3) · Google Gemini 2.0 Flash · SQLite · Python 3.10  

---

## 1. Project Objective

HR-Flow AI is a B2B AI-powered SaaS micro-product designed to automate the candidate resume screening pipeline for small and medium-sized enterprises (SMEs) within the restaurant and hospitality vertical in Almaty, Kazakhstan.

The core value proposition is the elimination of manual CV review overhead for restaurant operators — a demographic that typically lacks dedicated HR headcount. By leveraging a large language model (LLM) as the evaluation engine and Telegram as the delivery channel, HR-Flow AI transforms an unstructured, time-intensive hiring workflow into a deterministic, sub-minute screening operation accessible from any mobile device.

---

## 2. IT4IT Value Stream Mapping

### 2.1 S2P — Strategy to Portfolio

**Business Value Thesis:**  
Restaurant SMEs in Almaty operate under tight labour margins. The average hiring cycle for front-of-house and kitchen roles involves manual review of 40–100 CVs per vacancy, consuming 8–15 hours of a manager's operational time. HR-Flow AI collapses this to near-zero marginal cost per screening.

**Why Gemini 2.0 Flash:**

- **Cost arbitrage.** Google's Gemini 2.0 Flash model operates on a generous free tier (up to 1,500 requests/day), making it a zero-variable-cost inference backend for early-stage SME workloads. Compared to GPT-4o ($2.50/1M input tokens), Gemini Flash offers a >97% cost reduction at equivalent task quality for structured JSON extraction.
- **Latency profile.** Flash-tier models return structured evaluations in 1.2–2.5 seconds — well within the conversational UX threshold for Telegram interactions.
- **System instruction fidelity.** Gemini 1.5+ natively supports `system_instruction` at the model level, enabling deterministic persona injection (HR Director, Almaty restaurant chain) without prompt-prefix hacks.

**Portfolio alignment:** HR-Flow AI is positioned as a vertical AI agent — not a horizontal chatbot. The system prompt is domain-locked to hospitality hiring criteria (language proficiency in Kazakh/Russian/English, proximity to Almaty, HACCP knowledge), ensuring output relevance without fine-tuning.

---

### 2.2 R2D — Requirement to Deploy

**Architectural Process — AI-Directed Build Methodology:**

The entire technical artefact was constructed through a *Prompt Engineering as Architecture* (PEaA) methodology, where the Product Architect directed an AI coding assistant to materialise the system from natural-language specifications:

- **Database schema design.** The Architect specified the entity relationship (vacancies → applications, 1:N FK constraint) and the AI generated the `aiosqlite`-backed async DDL with `CREATE TABLE IF NOT EXISTS` idempotency, parameterised CRUD helpers, and FinOps aggregate queries — without a single line of hand-written SQL.
- **Python backend.** The modular package structure (`handlers/`, `services/`, `database/`) was dictated as an architectural directive. The AI produced production-grade code including frozen-dataclass configuration management, FSM state machines for multi-step conversation flows, and custom exception hierarchies for Google API error taxonomy.
- **Telegram interface layer.** The Architect specified UX flows (inline keyboards for vacancy selection, dual-input PDF/text resume ingestion, formatted score cards with visual bars), and the AI translated these into aiogram v3 Router registrations with proper filter chains and FSM gating.

**Key R2D artefacts produced:**

| Artefact | Purpose |
|---|---|
| `bot.py` | Application bootstrap, dispatcher wiring, polling lifecycle |
| `config.py` | Environment-driven settings with fail-fast validation |
| `setup_db.py` | Schema init + idempotent seed data (5 Almaty restaurant vacancies) |
| `Dockerfile` | Containerised deployment on `python:3.10-slim` |
| `requirements.txt` | Pinned dependency manifest with inline rationale |

---

### 2.3 R2F — Request to Fulfill

**Channel Selection — Why Telegram:**

- **Zero-friction onboarding.** Telegram has ~18M MAU in Kazakhstan. Restaurant managers already use it operationally — no app download, no SSO, no training required.
- **Rich interaction primitives.** Inline keyboards, document uploads (PDF/TXT), HTML-formatted responses, and callback queries provide a native-feeling UX without a custom frontend.
- **Bot API maturity.** The Telegram Bot API offers file download, user identity, and message state management out of the box — eliminating the need for authentication middleware.

**Environment Provisioning:**

The `setup_db.py` script ensures deterministic environment bootstrapping:

1. **Schema creation** — `init_db()` executes idempotent DDL (`CREATE TABLE IF NOT EXISTS`).
2. **Data seeding** — Checks `vacancies` table cardinality; if empty, inserts 5 production-representative test records with bilingual (RU/KZ/EN) requirements.
3. **Execution modes** — Callable standalone (`python setup_db.py`), inline (`python -c "..."`), or automatically on bot startup.

This three-mode provisioning strategy eliminates the "works on my machine" class of deployment failures.

---

### 2.4 D2C — Detect to Correct

**FinOps Strategy:**

- **Token metering.** Every `generate_content()` call extracts `usage_metadata.total_token_count` from the Gemini response object and persists it to the `applications.tokens_used` column.
- **Virtual cost projection.** The `/admin_stats` command aggregates total token consumption across all screenings and applies a configurable rate (`$COST_PER_MILLION_TOKENS`, default $0.075/1M) to project future spend — critical for capacity planning beyond the free tier.
- **Per-screening cost attribution.** The `applications.cost` column supports future per-request billing granularity.

**Error Monitoring & Resilience:**

| Failure mode | Detection | Correction |
|---|---|---|
| **401 — Invalid API Key** | `google.api_core.exceptions.PermissionDenied` | `AIAuthenticationError` → user-facing message, admin alert |
| **404 — Model not found** | `google.api_core.exceptions.NotFound` | Diagnostic via `test_gemini.py` → model enumeration |
| **429 — Quota exhausted** | `google.api_core.exceptions.ResourceExhausted` | `AIQuotaExceededError` → graceful degradation message |
| **Scanned PDF (no text)** | Empty string after PyMuPDF extraction | User-facing guidance with 3 alternative actions |
| **Malformed JSON response** | `json.JSONDecodeError` after markdown-fence stripping | `ValueError` → retry prompt |

**Diagnostic Tooling:**

The `test_gemini.py` script provides a 4-step pre-flight check:

1. Environment validation (API key presence)
2. Model enumeration (`genai.list_models()` with target matching)
3. Live inference test (prompt → response → token count)
4. Error taxonomy verification (401/403/404/429 handlers)

This diagnostic layer decouples API connectivity issues from application logic bugs — reducing mean-time-to-resolution (MTTR) for production incidents.

---

## 3. Reflection — Prompt Engineering as Architecture

### 3.1 The Paradigm Shift

Traditional software architecture involves translating requirements into code — the Architect writes UML, the developer writes Python. In the PEaA model, the Architect's deliverable is not a diagram but a *precisely-scoped natural-language directive*. The AI becomes a stateless compiler that transforms English into executable artefacts.

This inversion has profound implications for velocity: the full HR-Flow AI backend — 15 files, ~1,800 lines of production code, including database schema, AI integration, Telegram handlers, Dockerisation, and diagnostic tooling — was produced in a single architectural session without manual coding.

### 3.2 Challenges Encountered

- **Relational semantics in natural language.** Explaining a 1:N foreign key relationship (`applications.vacancy_id → vacancies.id`) and its cascade implications required more precise language than expected. The AI's default tendency is to generate isolated tables; enforcing referential integrity demanded explicit constraint specification.
- **API error taxonomy.** Directing the AI to implement granular exception handling for Google API errors (distinguishing `ResourceExhausted` from `PermissionDenied` from `InvalidArgument`) required knowledge of the `google.api_core.exceptions` class hierarchy — information the Architect had to explicitly inject into the prompt context.
- **State machine design.** The FSM flow (vacancy selection → resume upload → AI analysis → result) required careful sequencing in the directive. Early iterations conflated the vacancy handler and resume handler into a single module, losing the separation of concerns that enables independent testing.
- **FinOps instrumentation.** The concept of extracting `usage_metadata.total_token_count` from a Gemini response and persisting it for aggregate analysis was not a "natural" instruction — it required the Architect to understand both the SDK's response object structure and the downstream reporting requirements.

### 3.3 Key Takeaway

> **Prompt Engineering is not a substitute for architectural thinking — it is a new execution layer for it.**

The Architect must still possess deep technical knowledge: database normalisation, API error semantics, async I/O patterns, state machine design, and FinOps principles. What changes is the *medium of expression* — from imperative code to declarative specification. The cognitive load shifts from syntax to precision of intent.

---

**End of Report**
