# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Early-stage FastAPI backend for a money/transaction tracker. Postgres-backed via SQLAlchemy 2.0 (typed `Mapped` ORM). Read-only transaction endpoints exist so far; user auth and email import are scaffolded but not wired.

## Commands

There is no dependency manifest yet (no `requirements.txt`/`pyproject.toml`). Install deps manually:

```bash
pip install fastapi uvicorn "sqlalchemy>=2" "pydantic[email]" python-dotenv psycopg2-binary
```

- Run dev server: `uvicorn app.main:app --reload`
- API docs: http://127.0.0.1:8000/docs

Requires a `.env` at repo root with `DB_URL` (SQLAlchemy Postgres URL, e.g. `postgresql+psycopg2://user:pass@host/db`). Optional `DB_ECHO` (default `true`) toggles SQL logging.

No tests, linter, or migration tooling are set up.

## Architecture

Layered, one concern per package under `app/`:

- `routes/` — FastAPI routers (thin HTTP layer, `prefix="/api/v1/..."`). Only `transactions_router` is registered in `main.py`; `routes/user.py` is empty.
- `crud/` — data-access functions taking a `Session`. Re-exported via `crud/__init__.py`, so import from `app.crud` (not the submodule).
- `schemas/` — Pydantic request/response models (`ConfigDict(from_attributes=True)` to serialize ORM objects).
- `database/models.py` — SQLAlchemy ORM. `database/database.py` — engine, `SessionLocal`, and the `get_db` dependency.

Request flow: route → `Depends(get_db)` session → `crud` function → ORM objects → Pydantic response model.

### Things to know

- **Two `Base` classes exist** — one in `database/database.py` and one in `database/models.py`. The models use the one in `models.py`; that is the authoritative declarative base. Don't add tables against the `database.py` Base.
- **The DB schema is the source of truth.** `models.py` mirrors an existing Postgres schema (server-side `now()` defaults, `CHECK` constraints for `direction` CREDIT/DEBIT, `source` EMAIL/MANUAL, `amount > 0`). There is no migration setup — schema changes happen in the database, then are reflected here by hand.
- Three tables: `user_profiles`, `email_imports`, `transactions`. Transactions cascade-delete with the user; `email_import_id` is `SET NULL` on import deletion.
