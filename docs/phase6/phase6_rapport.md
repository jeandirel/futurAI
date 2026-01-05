# Rapport Phase 6 - Healing & Validation avancee

## Portee
Ajouter un healing simple autour de la generation RAG, avec retry si validation echoue.

## Actions realisees
- Endpoint /rag/generate/heal : generation MCQ avec retry (3 tentatives) si validation KO.
- Service Healing : ackend/app/services/healing.py (boucle retry + logs structlog).
- Tests : ackend/tests/test_healing.py pour verifier l'endpoint heal (unicite options, reponse presente).
- Plan Phase 6 : docs/phase6/phase6_plan.md.

## Etat actuel
- Healing operable au niveau RAG; validation basique (format/options/langue) integree.
- CI/lint/scripts toujours en place; tests heal a relancer si besoin.

## Risques / limites
- Validation encore minimale (longueur question/options, Bloom/SOLO, PII non controles).
- Healing limite au endpoint RAG; non branche sur le workflow jobs/orchestration.
- Generation reste placeholder (pas de LLM).

## Prochaines etapes (Phase 7)
- Etendre validation (longueur, Bloom/SOLO, PII).
- Integrer healing/retry dans le workflow jobs + metriques (taux retry, latence).
- Brancher un LLM et mesurer qualite (taux validation, latence, alignement).
