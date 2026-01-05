# Phase 5 - Validation & Qualite (plan)

Objectif : renforcer la generation avec validation stricte (format, unicite, alignement basique) et boucler avec Healing/Monitoring.

## Etapes prevues
- Validation MCQ : unicite options, reponse presente, langue supportee, format OK.
- Integration validation dans la generation RAG; rejeter/relancer si KO.
- Tests automatiques sur validation/generation.
- (Option) Debut Healing : regler generation si validation echoue (regen/fallback).
- (Option) Metriques rapides : taux validation OK/KO, latence.

## Actions deja en place
- Generation RAG placeholder + validation basique (unicite/options/langue) via `backend/app/services/validation.py` et endpoint `/rag/generate`.
- Tests RAG (search/generate).

## A faire
- Etendre validation (longueur question/options, controle champ bloom/solo).
- Brancher Healing ou boucle retry si validation KO.
- Enrichir tests (cas KO).
- (Option) ajouter metriques/alertes sur taux validation.
