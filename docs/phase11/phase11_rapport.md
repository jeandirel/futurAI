# Rapport Phase 11 - Déploiement & Ops

## Livrables
- Dockerfile backend (FastAPI/uvicorn) et Dockerfile Streamlit.
- docker-compose.yml (backend + Streamlit + Postgres + Redis).
- .dockerignore pour éviter d’embarquer les artefacts/caches.

## Comment déployer en local
1) Copier/adapter `config/.env` (non commité) avec DSN Postgres/Redis et variables LLM si dispo.
2) Lancer : `docker-compose up --build`
   - Backend : http://127.0.0.1:8000 (health, jobs, metrics)
   - Streamlit : http://127.0.0.1:8501
   - Postgres : port 5432 (DB `oneclickquiz`, extension vector activée via `shared_preload_libraries=vector`)
   - Redis : port 6379
3) Vérifier :
   - `curl http://127.0.0.1:8000/health` -> ok
   - `curl http://127.0.0.1:8000/metrics` -> snapshot JSON
   - `curl http://127.0.0.1:8000/jobs` -> liste

## Notes / limites
- Le service LLM reste à brancher (Inference API ou serveur local TGI/vLLM) ; config via `HF_API_BASE` et `HF_MODEL_ID`.
- Pas de pipeline CI/CD ajoutée ici (actions existantes ruff/pytest) ; à étendre si besoin (build image, push registry).
- Les volumes `pgdata` et `redisdata` sont créés par docker-compose.

## Prochaines étapes (si nécessaire)
- Ajouter un workflow GitHub Actions pour build/push des images (backend, streamlit).
- Ajouter un proxy HTTPS (nginx/traefik) et resserrer CORS.
- Documenter sauvegarde/restauration Postgres (pg_dump/pg_restore) et purge Redis.
