# Phase 8 - LLM / PII / Metriques (plan)

Objectif : remplacer le placeholder par un vrai LLM, renforcer PII/validation, et instrumenter les metriques (latence, retries, taux validation).

## Actions deja posees
- PII basique (email/tel) dans validation; redaction PII sur RAG search.
- Healing retry log (latency_ms).
- LLM toggle (settings.use_llm) + placeholder LLM client (`backend/app/services/llm.py`).

## A faire (Phase 8)
- Brancher un vrai LLM (OpenAI/Azure ou local) a la place du placeholder (respecter settings/use_llm).
- Etendre PII: regex plus robuste (nom propre, adresses), filtrage inputs RAG/generation.
- Metriques: logger latence generation/healing, taux retries, taux validation; (option) exporter vers dashboard.
- Tests e2e (RAG/generate/heal) avec LLM mock.
- Exposer ingestion/reindex + tests.

## Commandes utiles
- Toggle LLM: definir `USE_LLM=true` dans `.env` (apres avoir branche un vrai client).
- Tests cibles: `python -m pytest backend/tests/test_jobs.py backend/tests/test_rag.py backend/tests/test_healing.py backend/tests/test_validation.py`
