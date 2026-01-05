"""
Orchestrateur d'agents : génération -> validation -> feedback/fairness (optionnel).
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from backend.app.agents import FairnessAgent, FeedbackAgent, GenerationAgent, ValidationAgent
from backend.app.schemas.base import MCQItem


class AgentOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.generation = GenerationAgent(db)
        self.validation = ValidationAgent()
        self.feedback = FeedbackAgent()
        self.fairness = FairnessAgent()

    def generate_pipeline(
        self,
        subject: str,
        count: int = 1,
        k: int = 3,
        level: str = None,
        language: str = "fr",
        compute_feedback: bool = False,
        compute_fairness: bool = False,
        validation_llm: bool = False,
    ) -> dict:
        mcq_items: List[MCQItem] = self.generation.run(subject, count=count, k=k, level=level, language=language)
        self.validation.run(mcq_items, llm_check=validation_llm)

        feedback = self.feedback.run(mcq_items) if compute_feedback else None
        fairness = self.fairness.run(mcq_items) if compute_fairness else None

        return {
            "items": mcq_items,
            "feedback": feedback,
            "fairness": fairness,
            "validation_llm": self.validation.last_reports if validation_llm else None,
        }
