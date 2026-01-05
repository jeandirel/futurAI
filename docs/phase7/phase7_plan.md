# Phase 7 - Validation renforcee & Healing sur workflow (plan)

Objectif : finaliser la boucle generation/validation/healing avec validations plus strictes, tests negatifs, et integration dans le workflow jobs.

## Actions deja faites (phase 6)
- Healing simple sur `/rag/generate/heal` (retry 3x), validation basique, tests heal.
- Generation RAG placeholder, recherche pgvector OK, chunks charges.

## A faire (phase 7)
- Valider strictement question/options (longueur min/max, bloom/solo coherents, filtrage PII).
- Tests negatifs: MCQ invalides -> validation raise + healing retry observe.
- Brancher healing/validation dans jobs (fait) et ajouter un scenario de test.
- (Option) Ajouter metriques (taux retry, latence generation) dans logs.
- (Option) Preparation LLM reel pour generation (si dispo), sinon placeholder conserve.

## Commande tests cibles
- `python -m pytest backend/tests/test_jobs.py backend/tests/test_rag.py backend/tests/test_healing.py backend/tests/test_validation.py`
