# Phase 2 - Fondations techniques (S1)

Objectif : poser le squelette technique (API FastAPI, bases Postgres/pgvector, Redis), schemas de base et outillage CI/secrets.

## Livrables attendus
- Squelette backend FastAPI avec endpoint health et structure agents/services/core/schemas/db.
- Fichiers de config : `config/.env.example`.
- Requirements backend : `backend/requirements.txt`.
- Doc architecture de phase (ce fichier) et checklist CI/secrets (a venir).

## Taches realisees
- Arborescence backend creee (`backend/app/...`).
- Endpoint health: `backend/app/api/health.py` + `backend/app/main.py`.
- Settings Pydantic : `backend/app/core/settings.py`.
- Logging structlog de base : `backend/app/core/logging.py`.
- Schemas initiaux : `backend/app/schemas/base.py` (MCQ, enums), `backend/app/schemas/job.py` (job status, request/response).
- Middleware request-id + CORS : `backend/app/core/middleware.py`.
- Models SQLAlchemy : `backend/app/db/base.py`; session `backend/app/db/session.py`.
- Client Redis (stub) : `backend/app/services/redis.py`.
- API jobs (stub) : `backend/app/api/jobs.py`.
- Requirements initiales : FastAPI, UVicorn, pydantic, pydantic-settings, redis, psycopg2-binary, pgvector, structlog, SQLAlchemy, alembic.
- Config exemple : `config/.env.example` et `.env` genere (DSN/Redis locaux).
- README backend avec commandes de base.
- Alembic initialise : `backend/alembic.ini`, `backend/alembic/env.py`, `backend/alembic/versions/0001_init.py`.
- Tests de base : `backend/tests/test_health.py`, `backend/tests/test_jobs.py`; config pytest (`backend/pytest.ini`); deps dev (`backend/requirements-dev.txt`).
- CI de base : workflow GitHub Actions (`.github/workflows/ci.yml`) avec lint (ruff) et tests.
- Lint : config ruff (`backend/ruff.toml`).

## Taches restantes (phase 2)
- (Optionnel) Ajouter pre-commit et scripts run (`make` ou `invoke`).
- Completer schemas Pydantic (messages/documents) si besoin.
- (Optionnel) Ajouter mypy/flake8 si requis.

## Commandes utiles
- Installer deps backend : `pip install -r backend/requirements.txt`
- Installer deps dev tests : `pip install -r backend/requirements-dev.txt`
- Lancer l'API : `uvicorn backend.app.main:app --reload`
