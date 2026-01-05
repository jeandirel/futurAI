# Phase 10 – Observabilité & Stabilisation Finale

## Objectif
Préparer une version exploitable : exposition de métriques runtime, durcissement sécurité/PII, amélioration qualité (toxicity), et packaging prêt à déployer.

## Hypothèses
- Backend FastAPI fonctionnel (RAG, jobs, LLM + fallback).
- Évaluation/fairness batch existantes (phase 9).
- Postgres/Redis et CI (ruff/pytest) déjà en place.

## Livrables
- Endpoint de métriques (Prometheus ou JSON) : latence RAG/LLM, taux succès/échecs, healing.
- Toxicity checker amélioré (modèle ou API) avec hook dans validation/RAG.
- Guide d’exploitation (checks de démarrage, commande curl de santé/métriques, rotation logs).
- (Option) Artefact de déploiement léger (docker-compose ou image unique backend).

## Tâches
1) **Métriques runtime**
   - Ajouter un `/metrics` (Prometheus texte) ou `/stats` JSON exposant : requêtes RAG/LLM, latence p50/p95, taux d’erreur HF, healing_rate.
   - Instrumenter latence HF/RAG via middleware ou décorateur.

2) **Toxicité / PII**
   - Remplacer le placeholder par un classifieur de toxicité (HF pipeline ou API) avec seuil configurable.
   - Étendre PII regex (noms propres simples, IBAN/empreinte tel) ou brancher un outil dédié.

3) **CI / Tests**
   - Tests unitaires couvrant le nouvel endpoint metrics et les branches d’erreur LLM/toxicité (mocks).
   - Mettre à jour le workflow CI si besoin (marqueurs ou dépendances).

4) **Packaging**
   - Mettre à jour `config/.env.example` pour inclure les nouveaux paramètres (TOXICITY_MODEL, METRICS_ENABLED, etc.).
   - Ajouter un `docker-compose` ou instructions de build image backend.

5) **Documentation**
   - Rédiger `docs/phase10/phase10_rapport.md` avec les métriques observées, les risques restants.
   - Ajout d’un HOWTO “déploiement local” + commandes de vérification santé/métriques.

## Validation
- `/metrics` ou `/stats` retourne des valeurs non nulles après quelques hits.
- Tests CI passent avec les mocks (LLM/toxicité/metrics).
- Capacité à démarrer via env + curl santé/métriques documentés.
