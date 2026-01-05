# Rapport Phase 8 - LLM / PII / Metriques (partiel)

## Portee
Installer les points d'accroche pour un LLM, renforcer PII et metrages sur healing.

## Actions realisees
- Redaction PII basique dans RAG search (emails/phones).
- Validation etendue (question/options longueur, unicite, reponse, langue, PII simple).
- Healing logue la latence (latency_ms) et les retries.
- Toggle LLM (`settings.use_llm`) avec client Hugging Face Inference (`generate_mcq_hf`) et repli placeholder; generation appelle HF si token+model configures, sinon fallback.

## Etat actuel
- Generation LLM branchee via API Hugging Face (env `HF_API_TOKEN`, `HF_MODEL_ID`, `USE_LLM=true`) avec replis placeholder en cas d'echec reseau/API.
- Metriques via logs structlog (healing_success/healing_retry avec latency_ms); pas de dashboard.
- PII detection simple (regex email/tel) pour RAG search/validation.

## Risques / limites
- PII regex minimale; pas de filtrage nom/adresse, pas d'inspection des inputs utilisateur.
- Tests CI non relances ici (a lancer manuellement).
- LLM connecte via Hugging Face (API).

## Prochaines etapes (Phase 9)
- Mocker le client HF dans les tests pour CI sans reseau.
- Etendre PII et validation (Bloom/SOLO coherents).
- Metriques: taux validation, taux retries, latence (ajouter endpoints ou export).
