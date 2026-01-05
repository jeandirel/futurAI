# Phase 4 - Agent Generation & RAG (plan)

Objectif : brancher la generation de MCQ avec contexte RAG, exposer ingestion/retraitement, et commencer la validation qualitative.

## Etapes prevues
- Endpoints RAG : recherche de passages (fait) pour alimenter la generation.
- Generation : prompts RAG (LLM ou placeholder) + contraintes format MCQ; fallback si LLM echoue; logs/traces.
- Validation : checks format, unicite reponse, alignement Bloom/SOLO basique; rejet -> healing.
- Exposer ingestion/reindex (scripts ou API) avec filtrage PII et metadata (langue, chapitre).
- Metriques initiales : temps generation, taux rejets validation, taux healing.
- Tests basiques sur RAG/recherche/generation.

## Actions deja en place
- Chunks indexes dans Postgres (905) avec embeddings placeholder; table `chunks` accessible via pgvector.
- Endpoint RAG de recherche + generation MCQ simple (`POST /rag/search`, `POST /rag/generate`).
- Queue Redis + API jobs (stub), logging, schemas.
- CI/lint/tests (health/jobs/rag).

## A faire
- Brancher une vraie generation MCQ (LLM) et renforcer Validation.
- Filtrage PII avant ingestion/reindex; endpoint ingestion/reindex.
- Eval rapide: taux de passages retournes, latence RAG, sanite format MCQ.
