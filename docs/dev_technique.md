# Guide technique de developpement de la plateforme multi-robots OneClickQuiz

## 1. Stack proposee
- Backend API/orchestrateur : Python 3.12, FastAPI, Pydantic, Uvicorn.
- File/bus interne : Redis (queues) ou Celery/Arq pour planifier les taches d'agents.
- Stockage principal : Postgres + pgvector (index RAG + traces).
- Frontend : React (Next.js) ou Streamlit pour un dashboard de pilotage et de metriques.
- LLM : provider externe (ex. Azure OpenAI) + option open-source local (ex. Llama) via API unifiee.
- Observabilite : logs JSON (structlog), OpenTelemetry (traces), Prometheus/Grafana pour metrics.

## 2. Architecture logique
- Orchestrateur : recoit la requete (sujet, niveau, langue), cree un job, coordonne les agents et gere les timeouts/retry.
- Agents (taches asynchrones) :
  - Generation : produit MCQ + meta (taxonomie cible, langue, difficulte) en s'appuyant sur RAG.
  - Validation : verifie structure, unicite, alignement Bloom/SOLO (classifier few-shot/regles).
  - Feedback : genere explications multilingues, verifie tonalite (non toxique).
  - Equite : calcule flags de risque de biais (langue/culture/toxicite) et score fairness.
  - Healing : detecte echec ou incoherence, regenere ou ajuste prompt/modele, change de temperature/modele si besoin.
  - Archiviste/KG : gere ingestion des supports (cours, notes), creation d'index vectoriel, versionning des documents.
- Stockage :
  - Tables Postgres : `jobs`, `messages_agents`, `mcq`, `evals`, `fairness_metrics`, `documents`, `runs_healing`.
  - pgvector : embeddings des supports et des questions pour RAG et recherche de doublons.

## 3. Flux de donnee (happy path)
1) Frontend ou CLI appelle `/generate` avec {sujet, niveau, langue, contexte?}.
2) Orchestrateur cree un job, pousse tache `generation`.
3) Agent Generation requete LLM avec prompt + contexte (RAG) -> MCQ + meta.
4) Validation controle format, unicite reponse, alignement Bloom/SOLO. Si KO -> Healing.
5) Equite scanne la question/feedback (toxicite, stereotype, longueur/langue) -> score fairness. Si KO -> Healing.
6) Feedback produit une explication claire et courte, verifie tonalite.
7) Job termine -> resultat stocke (MCQ + meta + traces), retourne au frontend.

## 4. Prompts et garde-fous
- Templates Jinja avec sections : contexte, instruction, contraintes (format JSON), exemples, style.
- Contraintes strictes de sortie (JSON schema) + parsing/validation Pydantic.
- Timeouts et retry avec backoff; fallback modele (plus robuste) si 2 echecs.
- Filtrage PII/toxicite en entree/sortie (regex + modele de moderation).

## 5. RAG et gestion des supports
- Ingestion : parser PDF/Markdown, chunking (512-1024 tokens), embeddings (text-embedding-3 ou local).
- Index pgvector; stockage metadata (cours, chapitre, langue, version).
- Retrieval : kNN + rerank (optionnel) pour injecter 3-5 passages pertinents dans le prompt Generation/Validation.
- Versionning : conserver versions des documents; re-indexation incremental.

## 6. Evaluation et fairness
- Jeux de test : set MCQ gold (100+), repartis par langue/niveau/sujet.
- Metriques : F1 alignement Bloom/SOLO, acceptation par Validation, latency p95, taux healing.
- Fairness : demographic parity diff (acceptation), equalized odds diff (Validation), toxicity rate diff par langue/culture.
- Mitigation : rephrasing contraint, penalites stochastiques sur stereotypes, reweighting des exemples RAG.
- Scripts d'eval batch (pytest + scripts Python) + graphiques (matplotlib/altair) exposes dans le dashboard.

## 7. Tests et QA
- Unitaires : utils RAG, validators (format MCQ, unicite reponse), schemas Pydantic.
- Integre : pipeline end-to-end (generation -> validation -> feedback -> healing) sur echantillon fixe; snapshot outputs.
- Charge : Locust/k6 pour 50-100 requetes simultanees; surveiller latency, erreurs, saturation LLM/API.
- Securite : scans secrets (gitleaks), limites tailles input, sanitation HTML (si frontend).

## 8. Dashboard
- Vues : liste des jobs, detail d'un run (messages agents, prompts tronques), metriques live (latence, taux healing, fairness), alertes.
- Filtres : langue, niveau, cours, statut (OK/KO/healed).
- Exports : CSV/JSON des metriques et MCQ generes.

## 9. Deploiement
- Conteneurs Docker : api (FastAPI), worker (agents), redis, postgres+pgvector, frontend.
- Environnements : dev (hot reload), staging (tests de charge), prod (autoscaling API/worker).
- CI/CD : lint+tests (pytest) -> build images -> deploiement staging -> smoke tests -> prod.
- Secrets : variables d'env chiffees, pas de secrets en repo.

## 10. Runbook de production
- Alertes : taux echec >5%, latency p95 >4s, erreurs LLM >3% des calls, fairness diff > seuil.
- Playbooks : switch modele LLM, desactiver RAG si index HS, vider file en cas de tempete d'erreurs, reindexation documents.
- Sauvegardes : backups Postgres quotidiens; persistance volumes pour index.
