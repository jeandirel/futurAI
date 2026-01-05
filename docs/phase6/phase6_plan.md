# Phase 6 - Healing et qualite avancee (plan)

Objectif : boucler la generation avec healing/retry, enrichir validation, et preparer l'integration d'un vrai LLM.

## Actions initiees (faites)
- Healing simple sur generation RAG (/rag/generate/heal) avec retry 3x si validation KO.
- Validation basique (options uniques, reponse presente, langue supportee).
- Tests healing (endpoint heal) ajoutes.

## A faire (Phase 6)
- Etendre validation : longueurs min/max question/options, checks Bloom/SOLO plus stricts, filtrage PII.
- Ajouter metriques/minilog sur taux validation/retry (structlog).
- Brancher Healing sur l'orchestrateur jobs (pas seulement endpoint RAG).
- (Option) introduire un LLM reel pour la generation et mesurer impact (taux KO/latence).
- Tests negatifs (KO validation) et e2e healing.

## Commandes utiles
- Endpoint heal : POST /rag/generate/heal avec {"query":"...", "k":2}.
- Tests healing : python -m pytest backend/tests/test_healing.py.
