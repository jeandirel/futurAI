# Phase 0 - Cadrage

## Objectif
Lancer la plateforme de quiz multi-robots OneClickQuiz avec un cadre clair : besoins, publics, supports autorises et stack technique cible.

## Publics et langues
- Publics : eleves et professeurs (ecoles d'ingenieurs, universites); equipes pedagogiques; plateformes e-learning.
- Langues initiales : francais et anglais (extensible).

## Critères de reussite (rappels)
- Qualite : F1 Bloom/SOLO >= 93% sur set gold; taux healing > 85%.
- Fairness : >=3 biais identifies, >=3 metriques calculees (par ex. demographic parity diff, equalized odds diff, toxicity diff), mitigation appliquee et mesuree.
- UX : latence p95 < 4s; NPS > 7/10; taux acceptation validation > 90%.
- Fiabilite : downtime reduit de 15% vs baseline; taux de sorties valides élevé.

## Supports et périmètre donnees
- Documents sources autorises : cours/notes/diapos (PDF, slides), exemples MCQ valides, glossaires/formules du cours.
- Stockage des docs : dossier `data/raw`; versions indexees dans pgvector.
- Pas de PII collectee; si ajout d'etudiants ultérieurement, anonymisation et consentement requis.

## Stack cible (validee phase 0)
- Backend : Python 3.12, FastAPI, Uvicorn, Pydantic.
- Orchestration/queues : Redis + worker (Celery/Arq).
- Base : Postgres + extension pgvector.
- LLM : provider principal (ex. Azure OpenAI gpt-4o) + fallback open-source (Llama) via API unifiee.
- Frontend : React/Next.js (ou Streamlit pour MVP dashboard).
- Observabilite : logs JSON (structlog), OpenTelemetry, Prometheus/Grafana.

## Organisation et roles
- Backend/orchestrateur : dev backend.
- LLM/Prompts/RAG : specialiste LLM.
- Donnees/Fairness : data scientist pour annotation Bloom/SOLO et metriques de biais.
- Frontend : dev front pour dashboard.
- DevOps : CI/CD, conteneurs, monitoring.

## Risques initiaux et parades
- Donnees annotees Bloom/SOLO limitees : plan d'annotation interne (>=100 MCQ) + augmentation synthetique.
- Couts LLM : cache, batching, fallback open-source pour tests.
- Biais linguistiques/culturels : metriques systematiques par langue + rephrasing contraint.
- Latence/charge : tests charge precoces, parallélisation agents, fallbacks si LLM lent.

## Livrables de la phase 0
- Ce document de cadrage.
- Arborescence initiale creee (`docs/`, `data/` placeholders).
- Stack cible et roles valides.
