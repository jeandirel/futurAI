# Plan de taches et etapes (gestion de projet)

## Phase 0 - Cadrage (J0-J2)
- Clarifier besoin, publics (eleves/profs), langues supportees; valider criteres de reussite.
- Recenser supports autorises (PDF, slides, notes) et contraintes legales/PII.
- Choisir stack finale (LLM primaire/fallback, FastAPI, Redis, Postgres+pgvector, frontend).
- Planifier ressources (roles: backend, LLM/prompt, data/fairness, frontend, devops).

## Phase 1 - Donnees & annotation (J2-J5)
- Collecter/curer les cours et exemples; definir structure metadata (cours, chapitre, langue, version).
- Annoter set gold MCQ avec Bloom/SOLO (>=100 items); echantillons multi-langues.
- Definir liste de biais potentiels et cas limites (langue, genre, culture).
- Mettre en place scripts d'ingestion + stockage brut.

## Phase 2 - Fondations techniques (S1)
- Initialiser repo, CI (lint + tests), gestion secrets.
- Mettre en place FastAPI (squelette) + Postgres/pgvector + Redis.
- Definir schemas Pydantic pour jobs/messages/MCQ.
- Instrumentation minimale (logs JSON, traces).

## Phase 3 - Ingestion/RAG (S1-S2)
- Parser PDF/Markdown, chunking, embeddings; index pgvector.
- API d'ingestion/versionning des documents; re-indexation incr.
- Retrieval kNN + rerank (optionnel); tests de pertinence.

## Phase 4 - Agent Generation (S2)
- Templates prompts (Jinja) + contraintes JSON; integration RAG.
- Tests unitaires: format MCQ, unicite reponse, meta.
- Metriques: temps, taux de sorties valides.

## Phase 5 - Agent Validation (S2-S3)
- Regles syntactiques; classif Bloom/SOLO (few-shot + heuristiques).
- Seuils d'acceptation; renvoi vers Healing si KO.
- Tests integration generation->validation.

## Phase 6 - Agent Feedback & Equite (S3)
- Prompts feedback multilingues; checks tonalite/toxicite.
- Module Equite: scores fairness (toxicite, stereotypes, longueur/langue).
- Mitigations basiques (rephrasing contraint).

## Phase 7 - Agent Healing (S3-S4)
- Detecteurs: echec LLM, incoherence validation, scores fairness KO.
- Strategies: regeneration, changement de modele/temperature, resserrage de contraintes.
- Journalisation des actions et taux de succes.

## Phase 8 - Orchestration & workflow (S4)
- File de taches (Redis/Celery/Arq); orchestration des agents + timeouts/retry.
- Endpoint `/generate`; stockage des traces (jobs, messages_agents, runs_healing).
- Tests end-to-end sur echantillon fixe.

## Phase 9 - Evaluation & fairness (S4-S5)
- Scripts batch: F1 Bloom/SOLO, taux acceptation, latency p95, taux healing.
- Metriques fairness: demographic parity diff, equalized odds diff, toxicity diff par langue.
- Rapport avant/apres mitigation; visualisations.

## Phase 10 - Dashboard & UX (S5)
- Vues: liste jobs, detail run (prompts tronques, erreurs), metriques live (latence, healing, fairness).
- Filtres (langue, niveau, cours); export CSV/JSON.
- Mode CLI pour tests offline.

## Phase 11 - Durcissement & securite (S5-S6)
- Limites requetes, sanitation inputs, filtrage PII.
- Tests de charge (Locust/k6), resiliences (timeouts/fallbacks LLM).
- Alertes (taux echec > seuil, latency > seuil, fairness diff > seuil).

## Phase 12 - Deploiement (S6)
- Docker compose (api, worker, redis, postgres+pgvector, frontend).
- Pipeline CI/CD: build images, staging, smoke tests, prod.
- Backups Postgres quotidiens; surveillance.

## Phase 13 - Documentation & demo (S6-S7)
- README deploy/usage; diagrammes archi/sequence.
- Rapport projet (archi, fairness, limites, mitigation).
- Demo UI/CLI + jeu de test reproductible.

## Phase 14 - Pilotage continu
- Standups (3x/semaine), revue sprint hebdo, retro bi-hebdo.
- Suivi KPI: couverture tests, F1 Bloom/SOLO, taux healing, fairness diff, latency p95.
- Gestion risques (cout LLM, donnees limitees, latence) et plans de mitigation.
