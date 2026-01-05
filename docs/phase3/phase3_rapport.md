# Rapport Phase 3 - Ingestion / RAG

## Portee
Transformer les supports extraits en chunks, preparer les embeddings et l'index pgvector, et outiller l'ingestion.

## Actions realisees
- Chunking : `scripts/chunk_texts.py` -> `data/processed/chunks/chunks.jsonl` (905 chunks) depuis les `.txt` de `data/processed/`.
- Patching du chunker (evite boucle infinie si texte < taille chunk).
- Table `chunks` ajoutee (vector(128)) via Alembic v0002; creation appliquee dans Postgres.
- Embeddings placeholder deterministes : `backend/app/services/embeddings.py` (hash -> vecteur 128).
- Ingestion DB via TSV + psql (`scripts/build_chunks_tsv.py` + `scripts/load_chunks.sql`) : table `chunks` peuplee avec 905 lignes; `alembic_version` mis a jour en `0002_chunks`.

## Etat actuel
- Fichiers : chunks JSONL et TSV; table `chunks` contient 905 lignes (verifiee via psql).
- Tests backend toujours OK (`python -m pytest`).
- CI/lint restent operationnels.
- Ingestion DB faite via `docker exec ... psql -f /tmp/load_chunks.sql` (chunks.tsv copie).

## Points restants / risques
- Embeddings placeholder : remplacer par un vrai modele (ex. sentence-transformers) + gestion des secrets si provider externe.
- API ingestion/reindex non exposee (scripts/import manuel).
- Filtrage PII avant index non implemente (a ajouter).
- `chunk_ingest.py` non utilise pour ingestion finale (bloquait sur env), ingestion faite via TSV/psql.

## Prochaines etapes (Phase 4)
- Agent Generation : prompts RAG sur cours, validation format MCQ, metriques de qualite.
- Ajouter endpoints ingestion/reindex + retrieval, filtrage PII, rerank eventuel.
