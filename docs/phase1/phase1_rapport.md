# Rapport Phase 1 - Donnees & Annotation

## Portee
Constitution et preparation du corpus de cours, extraction texte, annotations MCQ gold (Bloom/SOLO), cartographie des biais initiaux et outillage de validation.

## Actions realisees
- Collecte des supports et depot dans `data/raw/` (PDF cours/rapports + manifest.csv).
- Extraction texte des PDF vers `data/processed/` via `scripts/extract_pdf_text.py` (log des pages et fichiers non-PDF ignores).
- Creation du manifest des sources : `data/raw/manifest.csv`.
- Constitution du jeu gold : `data/annotations/mcq_gold.jsonl` (105 items FR/EN) avec labels Bloom/SOLO, difficulte, langue, topic, source, notes.
- Seed initial : `data/annotations/mcq_seed.jsonl`.
- Validation schema JSONL (MCQ) avec `scripts/validate_mcq_jsonl.py` (passes sur seed et gold).
- Cartographie des biais et cas limites : `docs/phase1/biais_initiaux.md`.
- Documentation de phase mise a jour : `docs/phase1/phase1_donnees_annotation.md` (statut, livrables).

## Artefacts
- Corpus brut : `data/raw/` (PDF) + `data/raw/manifest.csv`.
- Corpus texte : `data/processed/` (txt extraits des PDF).
- Annotations : `data/annotations/mcq_gold.jsonl` (105 items), `data/annotations/mcq_seed.jsonl`.
- Scripts : `scripts/extract_pdf_text.py`, `scripts/validate_mcq_jsonl.py`, `scripts/README.md`.
- Biais initiaux : `docs/phase1/biais_initiaux.md`.
- Plan et statut phase : `docs/phase1/phase1_donnees_annotation.md`.

## Metrique de progression
- Volume annotations gold : 105 items (objectif atteint >=100).
- Langues : FR/EN presentes; difficulte et topics varies (contexte projet/tech/fairness).
- Validation schema : OK (aucune erreur detectee).

## Risques restants / limites
- Gold set encore petit pour couvrir tous les chapitres des cours (uniformite topics a surveiller).
- PPTX non extraits (convertir si necessaire pour enrichir le RAG).
- Annotation faite en une passe : prevoir double-lecture echantillon (10-20%) pour harmoniser labels Bloom/SOLO.

## Prochaines etapes (Phase 2 - Fondations techniques)
- Initialiser FastAPI + Postgres/pgvector + Redis (squelette backend + schemas Pydantic). fait (phase 2 en cours)
- Mettre en place CI (lint/tests) et gestion des secrets (en cours/a faire).
- Definir models de donnees (jobs, messages_agents, mcq, documents) et migrations initiales. fait
- Instrumentation logs JSON + traces de base. fait
