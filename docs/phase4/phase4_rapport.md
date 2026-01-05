# Rapport Phase 4 - Generation & RAG

## Portee
Connecter la generation MCQ sur le RAG (chunks en base) et fournir endpoints/test de recherche et generation.

## Actions realisees
- Endpoint RAG recherche : `POST /rag/search` (retourne top-k chunks pgvector).
- Endpoint RAG generation : `POST /rag/generate` (MCQ simple base sur top-k RAG, placeholder sans LLM).
- Services : recherche pgvector (`backend/app/services/rag.py`), generation placeholder (`backend/app/services/generator.py`).
- Schemas RAG : `backend/app/schemas/rag.py`.
- Tests : `backend/tests/test_rag.py` (search + generate).
- Docs : plan Phase 4 (`docs/phase4/phase4_plan.md`).

## Etat actuel
- API health/jobs/rag operationnelle; tests pass (pytest) hors execution locale interrompue.
- Chunks en base (905) exploits par RAG; embeddings placeholder.

## Risques / limites
- Generation MCQ encore placeholder (pas de LLM, options generiques).
- Pas de filtrage PII; pas d’endpoint ingestion/reindex expose.
- Validations cognitives (Bloom/SOLO) non renforcees; Healing non branche sur RAG.

## Prochaines etapes (Phase 5)
- Brancher LLM pour generation + validation stricte format/alignment.
- Ajouter endpoint ingestion/reindex + filtrage PII + rerank.
- Evaluer latence, qualite MCQ, taux rejets/Healing; durcir tests automatiques.
