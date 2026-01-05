# Rapport Phase 9 - Evaluation & Fairness

## Portee
Evaluer la qualite et l’equilibre des generations (acceptation, latence, fairness) et fournir des moyens de suivi.

## Actions realisees
- Script batch `scripts/eval_batch.py` (JSON/JSONL) calcule : taux d’acceptation (validation), healing rate, latence p50/p95, F1 Bloom/SOLO si labels de reference, fairness (par groupe/langue) avec ecarts d’acceptation/toxicite/healing.
- Utilitaires d’evaluation dans `backend/app/services/evaluation.py` pour instrumenter les calculs et faciliter les tests.
- `.env.example` mis a jour (LLM: HF_API_BASE, HF_FALLBACK_MODEL).

## Comment tester
```
python scripts/eval_batch.py data/annotations/mcq_gold.jsonl
# ou en regroupant par un autre champ
python scripts/eval_batch.py data/annotations/mcq_gold.jsonl --group-field language --output metrics_phase9.json
```
Le script affiche les metriques (acceptance, latence si disponible, fairness par groupe). Si les champs `bloom_true`/`solo_true` sont presents, le F1 est calcule, sinon il reste a Null.

## Risques / limites
- Pas de classifieur de toxicite avance : simple liste de mots clefs (a remplacer par un modele).
- Les metriques fairness supposent un champ de groupe (par defaut la langue) ; si les attributs sensibles ne sont pas fournis, l’analyse reste partielle.
- F1 Bloom/SOLO ne se calcule que si les labels de reference sont fournis dans les donnees.

## Prochaines etapes
- Brancher un classifieur de toxicite (ou API) et enrichir les attributs de groupe (si disponibles) pour une fairness plus fine.
- Ajouter des tests unitaires specifiques sur l’evaluation (mocks) dans la CI.
- Alimenter un endpoint `/metrics` (Prometheus ou JSON) pour exposer ces indicateurs en production.
