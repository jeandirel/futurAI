# Phase 1 - Donnees & annotation (J2-J5)

Objectif : preparer les supports de cours, constituer un set gold annote Bloom/SOLO et cartographier les biais de depart.

## Livrables attendus
- Corpus source range dans `data/raw/` (cours, slides, notes, exemples MCQ valides).
- Script d'ingestion initial (placeholder dans `scripts/`) pour copier/valider les fichiers.
- Jeu gold MCQ annote (>=100 items) dans `data/annotations/` avec labels Bloom/SOLO + langue/niveau.
- Liste des biais potentiels et cas limites (langue, genre, culture, terminologie) dans `docs` (peut etre integree ici).

## Taches detaillees
1) Collecter les supports autorises et les deposer dans `data/raw/`.
2) Verifier formats (PDF/MD/texte) et droits d'usage; exclure PII.
3) Compiler des exemples MCQ deja valides (si dispos) -> fichier `data/annotations/mcq_seed.jsonl`.
4) Annoter manuellement >=100 MCQ avec Bloom/SOLO, langue, difficulte -> `data/annotations/mcq_gold.jsonl`.
5) Noter les biais potentiels et cas limites dans `docs/biais_initiaux.md` (langue, genre, culture, jargons).
6) Preparer un schema JSON pour les MCQ annotes (question, options, reponse, bloom, solo, langue, source).

## Schema suggere (JSONL)
```json
{
  "question": "Texte de la question",
  "options": ["A", "B", "C", "D"],
  "answer": "A",
  "bloom": "apply|analyze|evaluate|create|remember|understand",
  "solo": "prestructural|unistructural|multistructural|relational|extended",
  "difficulty": "easy|medium|hard",
  "language": "fr|en",
  "topic": "nom_du_cours_ou_chapitre",
  "source": "nom_du_doc_ou_url",
  "notes": "commentaires/justifications (optionnel)"
}
```

## Planning (indicatif)
- J2 : collecte supports, creation des fichiers seed.
- J3 : annotation manuelle (50 items), redaction biais initiaux.
- J4 : annotation manuelle (50+ items), verification croisee.
- J5 : consolidation du jeu gold, verification du schema, depot dans `data/annotations/`.

## Risques & parades (Phase 1)
- Volume d'items gold insuffisant : generer des brouillons via LLM puis valider manuellement.
- Divergence d'annotation : faire une double lecture sur un echantillon (10-20%) et harmoniser.
- Biais linguistiques : equilibrer fr/en dans le jeu gold; inclure sujets varies.

## Statut Phase 1
- Corpus PDF place dans `data/raw/` et extrait en texte dans `data/processed/` (via `scripts/extract_pdf_text.py`).
- Manifest des sources : `data/raw/manifest.csv`.
- Jeu gold : `data/annotations/mcq_gold.jsonl` (105 items, FR/EN, Bloom/SOLO) valide avec `scripts/validate_mcq_jsonl.py`.
- Seeds : `data/annotations/mcq_seed.jsonl`.
- Biais cartographies : `docs/biais_initiaux.md`.
