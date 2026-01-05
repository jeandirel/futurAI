# Backend (FastAPI)

## Installation
```
pip install -r backend/requirements.txt
```

## Lancer le serveur (dev)
```
uvicorn backend.app.main:app --reload
```
Sante: `GET http://localhost:8000/health` -> `{"status": "ok"}`.

## Configuration
- Copier `config/.env.example` vers `.env` et ajuster `POSTGRES_DSN`, `REDIS_URL`.
- Settings charges via `backend/app/core/settings.py`.

## Structure
- `app/api` : routes FastAPI (health, endpoints a venir).
- `app/core` : settings, logging.
- `app/schemas` : models Pydantic (MCQItem, jobs, etc.).
- `app/agents` : logiques d'agents (a venir).
- `app/services` : clients LLM/RAG/db (a venir).
- `app/db` : gestion DB/migrations (a venir).

## Alembic (migrations)
- Config: `backend/alembic.ini`
- Env: `backend/alembic/env.py`
- Versions: `backend/alembic/versions/0001_init.py`
- Commandes:
```
alembic -c backend/alembic.ini upgrade head
alembic -c backend/alembic.ini revision --autogenerate -m "message"
```
Assurez-vous que Postgres est accessible et que l'extension `vector` est installee (`CREATE EXTENSION IF NOT EXISTS vector`).

## A faire (Phase 2)
- CI (lint/tests), pre-commit optionnel.
- Schemas manquants (jobs/messages complets, documents) et migrations Alembic.
- Clients DB/Redis et configurateurs.
- Logging structlog enrichi (trace-id, correlation-id).
