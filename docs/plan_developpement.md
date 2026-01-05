# Plan de developpement — IA multi-agent auto-corrective pour OneClickQuiz

## Choix du projet
- Projet retenu : **Multi-Agentic AI with Self-Healing Capabilities for Adaptive Cognitive Alignment in OneClickQuiz** (page 12 du PDF projets).
- Raison : aligne le mieux les consignes de `instructions.pdf` (IA agentique, domaine education, evaluation des biais, mitigation, interface utilisateur) et le barreme `Evaluation Grid.pdf` (multi-agents, integration LLM, metriques de fairness).
- Objectif : proposer des quizzes d’ingenierie cognitivement alignes (Bloom + SOLO), resilients aux erreurs (auto-healing) et equitables (reduire biais linguistiques/culturels).

## Critères de reussite (cibles mesurables)
- Architecture A01 : >=4 agents roles clairs + coordination explicite (file/réseau) + diagramme d’architecture.
- LLM A02 : prompts templates (Jinja), guardrails, gestion de contexte (RAG/KB), timeouts + tests de regression.
- Alignement cognitif : F1 >=93% sur classif Bloom/SOLO vs gold set humain et >=25% gain vs baseline mono-agent.
- Self-healing : >85% taux de remediation automatique des erreurs detectees; reduction du downtime agent de 15% vs baseline.
- Qualite quiz : taux d’acceptation humain >90%, hallucinations <3% sur echantillon controle.
- Fairness/Biais : identifier >=3 biais; calculer >=3 metriques (demographic parity diff, equalized odds diff, toxicity rate diff); appliquer >=1 mitigation (rephrasing contraint, re-weighting, prompt debias); visualisations des metriques.
- UX : latence p95 <4s, NPS >7/10 sur sondage pilote (>=10 etudiants).
- Documentation : rapport format academique (archi, fairness, limites); README deploiement; demo UI/CLI.

## Portee fonctionnelle
- Generation adaptative de questions (MCQ) alignees aux niveaux Bloom/SOLO.
- Feedback automatique par agent dedie, avec detection de biais linguistique/culturel.
- Orchestration multi-agent (generation, feedback, validation cognitive, healing).
- Tableau de bord web: suivi des generations, alertes d’erreurs, visualisation metriques de fairness/perf.
- Mode CLI pour tests offline/reproductibles.

## Architecture cible
- **Agents principaux**  
  - `Agent.Generation`: construit question + distracteurs + metadata (taxonomie, difficulte).  
  - `Agent.Validation`: verifie coherence (solutions, alignement Bloom/SOLO), passe tests unitaires (structure).  
  - `Agent.Feedback`: genere feedback nuance (multilingue), controle biais (toxicity, stereotypes).  
  - `Agent.Healing`: detecte panne/mauvais alignement (regles + anomalies) et relance generation ou ajuste prompt.  
  - (Option) `Agent.KB`: gere contexte RAG (cours, exemples, grille d’evaluation).  
  - (Option) `Agent.Observer`: collecte logs/metriques pour fairness et qualite.
- **Coordination** : orchestrateur (FastAPI/Task queue) + bus interne (Redis/SQLite queue) + schema de messages JSON schema/Pydantic.
- **Connaissances** : base vectorielle (pgvector/Chroma) avec cours/exemples + grille Bloom/SOLO + patrons de feedback.
- **LLM** : modele heberge (OpenAI/azure ou local) + prompts templates; fallback vers modele plus petit en cas d’echec.
- **UI** : dashboard (React/Next ou Streamlit) + vues: runbook healing, metriques fairness, historique generations.
- **Observabilite** : logging structuré (JSON), traces (OpenTelemetry), alertes sur erreurs > seuil.

## Roadmap detaillee (sprints de 1 semaine indicatifs)

### Phase 0 — Cadre & donnees (jour 0-2)
- Valider use case, utilisateurs cibles, langues (FR/EN).  
- Definir jeux de reference: corpus cours, exemples MCQ, etiquettes Bloom/SOLO gold (>=100 items).  
- Cartographier biais potentiels (langue, genre, discipline, complexite).  
- Choisir stack (Python 3.12, FastAPI, Postgres/pgvector, React ou Streamlit, LLM provider).

### Phase 1 — Spikes techniques (jour 2-5)
- Spike LLM: tester 2 modeles (gpt-4o ou equivalent open-source) sur 10 prompts; mesurer cout/latence.  
- Spike RAG: comparer index simple vs reranking; mesurer precision.  
- Spike validation cognitive: prototyper classif Bloom/SOLO (few-shot + regles).  
- Decision doc: choix modele, index, orchestrateur.

### Phase 2 — Architecture & fondations (semaine 2)
- Concevoir schemas messages (Pydantic) entre agents; definir contrat de retry/timeouts.  
- Mettre en place repo, CI lint/test, gestion secrets.  
- Impl. FastAPI + endpoints orchestrateur; file interne (Redis/SQLite queue).  
- Stockage: Postgres + extension pgvector + tables runs/logs/metriques.  
- Logging structuré + traces basiques.

### Phase 3 — Agent Generation (semaine 3)
- Templates prompts pour MCQ (inputs: sujet, niveau, langue, taxonomie cible).  
- Integration RAG pour contexte de cours.  
- Tests unitaires: format MCQ, unicite reponse, longueur.  
- Metriques: temps generation, taux reponses valides.

### Phase 4 — Agent Validation (semaine 3-4)
- Regles syntactiques (format, options, reponse).  
- Classif Bloom/SOLO (few-shot + heuristiques) => score alignement.  
- Rejet ou retour a Healing si score < seuil; log des raisons.

### Phase 5 — Agent Feedback (semaine 4)
- Prompt feedback multilingue; inclusion consignes d’ethique.  
- Detection biais/toxicite (Perspective API ou modele offline) sur feedback et enonce.  
- Metriques: toxicity rate, longueur feedback, clarte (sondage rapide).

### Phase 6 — Agent Healing (semaine 5)
- Detecteurs: echec LLM, incoherence validation, metriques hors seuil.  
- Strategies: regeneration, changement de temperature, changement de modele, renforcement de contraintes; compteur de tentatives.  
- Journalisation des actions de self-healing + taux de succes.

### Phase 7 — Fairness & biais (semaine 5-6)
- Definir sous-groupes: langue (FR/EN), niveau etudiant, specialite.  
- Metriques: demographic parity diff sur acceptation quiz, equalized odds sur validation, toxicity diff par langue; visualisation.  
- Mitigation: rephrasing contraint, penalite dans prompt pour stereotypes, reweighting des exemples RAG.  
- Rapport fairness + tests automatises (scripts eval).

### Phase 8 — Dashboard & UX (semaine 6)
- Vues: liste des runs, detail run (messages agents), metriques alignement, fairness charts, alerts healing.  
- Filtres par langue/niveau; export CSV/JSON.  
- Mode CLI pour generation batch + eval offline.

### Phase 9 — Evaluation finale & durcissement (semaine 7)
- Campagne eval: 200 quizzes, annotation humaine (qualite, alignement, biais).  
- Tests de charge (100 requetes concurrentes) + resiliences (latence p95).  
- Durcissement securite: limits tokens, filtrage inputs, politique PII.

### Phase 10 — Documentation & livraison (semaine 8)
- README dev/deploiement, diagrammes d’archi/sequence.  
- Rapport academique: archi, fairness, metriques, mitigation, limites, recommandations.  
- Demo video + jeu d’essai reproductible.  
- Plan de maintenance (monitoring, seuils alertes, runbook incidents).

## Plan d’evaluation (aligne Evaluation Grid)
- A01: revue archi multi-agent (doc + tests integration orchestrateur).  
- A02: choix LLM justifie, prompts templates, gestion erreurs/timeout.  
- B01: doc des biais identifies (>=3) avec exemples.  
- B02: scripts calcul metriques fairness + graphiques.  
- B03: mitigation implementee + mesure avant/apres.  
- Bonus: open-source des prompts/agent harness + visualisations claires.

## Donnees & governance
- Sources: cours/formats MCQ existants, taxonomies Bloom/SOLO, logs OneClickQuiz.  
- Stockage PII: eviter; sinon chiffrement en base + anonymisation.  
- Versioning des prompts et datasets (DVC ou Git LFS).  
- Garde-fous: filtres PII, limites tokens, content safety.

## Tests & QA
- Unitaires: validation format MCQ, schemas messages, utils RAG.  
- Integration: scenario end-to-end (Generation -> Validation -> Feedback -> Healing).  
- Evaluation offline: scripts pour F1 alignement, metriques fairness, taux healing.  
- E2E UI/CLI: Cypress/Playwright ou tests CLI snapshot.  
- Monitoring: alerts sur taux echec agent, latency, diff fairness > seuil.

## Risques & mitigations
- Cout LLM : prevoir modele open-source + cache; batching.  
- Donnees etiquetees Bloom/SOLO limitees : annotation rapide interne + augmentation donnees synthetiques.  
- Latence multi-agent : parallelliser Generation/Feedback quand possible; timeouts et fallbacks.  
- Compliance: aucune donnee patient/PII; evaluation legal si extension a utilisateurs finaux.

## Deploiement cible
- Environnement: Docker compose (API + Redis + Postgres/pgvector + frontend).  
- CI/CD: tests + lint + scan secrets; deploiement staging puis prod.  
- Observabilite: dashboards (Grafana) + alertes (latence, erreurs, fairness drift).

## Suivi projet
- Ceremonies: standup 3x/semaine, revue sprint hebdo, retro bi-hebdo.  
- Kanban/board avec epics: Archi, Agents, Fairness, Dashboard, Deploiement, Documentation.  
- KPI d’avancement: stories terminees, couverture tests, metriques ciblees atteintes.
