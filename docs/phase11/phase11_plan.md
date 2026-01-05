# Phase 11 – Déploiement & Opérations

## Objectif
Passer d’un environnement de dev à une mise en prod maîtrisée : packaging, CI/CD, observabilité en place, procédures d’exploitation et sécurité.

## Hypothèses
- Backend FastAPI opérationnel, frontend Streamlit disponible.
- Base Postgres/pgvector et Redis déjà configurées.
- CI basique (ruff/pytest) existante.
- LLM local ou distant à brancher ultérieurement (non bloquant pour le déploiement).

## Livrables
- Manifeste de déploiement (docker-compose ou chart simple) incluant backend + Redis + Postgres + éventuel serveur LLM.
- Pipeline CI/CD (lint/tests + build image + déploiement staging).
- Documentation d’exploitation (start/stop, variables d’environnement, sauvegardes DB, rotation logs, supervision).
- Procédure de reprise (restauration sauvegarde, régénération des embeddings le cas échéant).

## Tâches
1) **Packaging**
   - Dockerfile backend (FastAPI + uvicorn) et docker-compose avec Postgres/Redis/Streamlit.
   - Variables d’env harmonisées (`config/.env.example`), secrets via fichiers ou env.
2) **CI/CD**
   - Étendre le workflow GitHub Actions : lint/tests, build image, push registry (staging).
   - Option: déploiement auto sur une cible (ou script de déploiement manuel documenté).
3) **Observabilité & logs**
   - Brancher `/metrics/prom` à un Prometheus distant (doc), config logs structurés.
   - Healthcheck Docker/compose.
4) **Sécurité & backups**
   - Checklist : secrets non committés, CORS resserré, HTTPS (proxy Nginx ou autre).
   - Procédure de sauvegarde/restauration Postgres, purge Redis.
5) **Documentation**
   - Rédiger `docs/phase11/phase11_rapport.md` avec instructions de déploiement, commandes de vérif, plan de reprise.

## Validation
- `docker-compose up` lance backend/redis/postgres (+ optionnel Streamlit) et le healthcheck répond.
- CI passe et produit une image utilisable.
- Procédures d’exploitation documentées et testées sur un environnement de test.
