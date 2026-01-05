# Phase 3 - Ingestion/RAG (plan)

Objectif : exploiter les supports de cours pour le RAG (chunking, embeddings, index pgvector) et exposer ingestion/reindex. Le tout avec filtration PII et metadata (langue/sujet).

## Etapes prevues
- Chunking : transformer les `.txt` de `data/processed/` en JSONL de chunks (taille 1500, overlap 200) -> `data/processed/chunks/chunks.jsonl`.
- Embeddings : generer des vecteurs (placeholder hash deterministe pour l'instant) et indexer dans Postgres/pgvector.
- Tables : `documents`, `chunks` (id, source, position, text, embedding, doc_id, created_at).
- Endpoints/CLI : ingestion et reindexation (todo si besoin API).
- Verifs : nombre de chunks, presence metadata (source, position), tests basiques.
- Filtrage PII (a ajouter en amont si necessaire).

## Commandes
- Chunking : `python scripts/chunk_texts.py`
- Ingestion DB : `python backend/app/services/chunk_ingest.py`
- Migrations : `python -m alembic -c backend/alembic.ini upgrade head`

## Definition d'achevement Phase 3
- Chunks generes et stockes (JSONL) + indexes dans Postgres (table `chunks` avec embeddings).
- Script d'ingestion operationnel.
- Doc de phase et verification (compte chunks, samples).
- (Option) endpoint ingestion/reindex si expose via API.
