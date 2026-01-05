# Phase 9 – Industrialisation & Qualité ML/Produit

## Objectif
Finaliser une version prête à l’usage : LLM stable (HF router), observabilité (metrics/logs), robustesse (tests, CI), sécurité (PII), et packaging (infra légère).

## Hypothèses
- Postgres/Redis déjà en place, données chunkées et index vector OK.
- CI existante (ruff/pytest) mais à étendre.
- LLM distant via HF router (modèle public ou accepté avec le token).

## Livrables
- Client LLM opérationnel (modèle accessible) + fallback robuste.
- Tableau de bord minimal : métriques RAG/génération/healing exposées (Prometheus/endpoint JSON).
- Jeux de tests élargis (mocks LLM, RAG, jobs).
- Documentation d’exploitation (README phase 9) et rapport.

## Tâches
1) **LLM fiable**
   - Choisir un modèle servi par `router.huggingface.co` (ex. `HuggingFaceH4/zephyr-7b-beta`) ou accepter le modèle gated choisi.
   - Ajouter logs explicites sur succès/échec HF, et code de statut.
   - Timeout/retry léger (1 retry) et fallback placeholder clair.

2) **Observabilité**
   - Exposer un endpoint `/metrics` ou `/stats` (JSON) : taux de succès génération, échecs HF, temps moyen healing, nombre de requêtes RAG.
   - Instrumenter timers (latence HF / RAG) avec `time.perf_counter`.

3) **Tests & CI**
   - Ajouter tests unitaires pour le client HF mocké (réponses 200/404/401 -> fallback).
   - Tests RAG/validation déjà en place : couvrir les nouvelles métriques.
   - Mettre à jour workflow CI pour inclure ces tests (si besoin de marqueur).

4) **Packaging / Config**
   - Mettre à jour `config/.env.example` avec les nouveaux paramètres (`HF_API_BASE`, `HF_FALLBACK_MODEL`).
   - Ajouter une section “Exploitation” dans les docs avec les commandes de vérif (curl /health, /metrics).

5) **Documentation**
   - Rédiger `docs/phase9/phase9_rapport.md` (résumé actions, risques restants, next steps).
   - Ajouter un court HOWTO “changer de modèle HF” (env vars + test direct).

## Validation finale
- `pytest` (avec mocks HF) passe.
- Appel `/jobs/generate` retourne un MCQ non-placeholder avec un modèle HF accessible.
- Endpoint métriques renvoie des valeurs non vides après quelques requêtes.
