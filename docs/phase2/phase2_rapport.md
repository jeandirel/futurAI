# Rapport Phase 2 - Fondations techniques

## Portee
Mettre en place le socle technique : API FastAPI, DB Postgres/pgvector, Redis, schemas, migrations, logging, queue, tests et CI de base.

## Actions realisees
- Backend FastAPI structuree (`backend/app/...`), endpoint sante `/health`.
- Jobs stub (`/jobs/generate`, `/jobs/{id}`) avec enqueue Redis.
- Settings (pydantic-settings), CORS + middleware request-id, logging structlog.
- Schemas Pydantic (MCQ, Job), models SQLAlchemy (jobs, agent_messages, mcq, documents, fairness_metrics), session DB.
- Migrations Alembic init + appliquées sur Postgres (pg-oneclick) avec extension `vector`.
- Queue Redis (client + enqueue/dequeue).
- Config `.env` (DSN Postgres, Redis) et `config/.env.example`.
- Requirements backend + dev (tests).
- Tests : health et jobs OK (`python -m pytest`).
- Lint : ruff config.
- CI : GitHub Actions (lint + tests).
- Conteneurs en place : `pg-oneclick` (Postgres+pgvector), `redis-oneclick`.

## Artefacts
- Code : backend (API, core, schemas, db, services, tests), configs (`config/.env`, `backend/ruff.toml`), CI (`.github/workflows/ci.yml`), migrations (`backend/alembic/...`).
- Docs : `docs/phase2_fondations.md` (plan phase 2), `docs/phase2_rapport.md` (ce fichier).

## Statut tests
- Tests passes : `python -m pytest` (health + jobs). Warnings Pydantic (deprecation Config/field length) sans impact fonctionnel.

## Risques/points restants
- Pas de pre-commit ni mypy/flake8 (optionnel).
- Queue/agents encore stubs (Phase 3+).
- Harmoniser versions Pydantic/uvicorn avec autres outils si nécessaires (vérifier compatibilité CI).

## Prochaines etapes (Phase 3)
- Ingestion RAG : chunking, embeddings, index pgvector, endpoints d’ingestion, re-indexation.
- Tests de pertinence et contrôle PII avant indexation.
- Eventuel rerank + metadata (langue, chapitre) pour retrieval.
