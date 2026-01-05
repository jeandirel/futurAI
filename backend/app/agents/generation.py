"""
Generation agent: produit des MCQ en s'appuyant sur RAG + healing.
"""

from typing import List

from sqlalchemy.orm import Session

from backend.app.schemas.base import MCQItem
from backend.app.schemas.rag import RAGQuery
from backend.app.services.healing import heal_generation


class GenerationAgent:
    def __init__(self, db: Session):
        self.db = db

    def run(self, subject: str, count: int = 1, k: int = 3, level: str = None, language: str = "fr") -> List[MCQItem]:
        items: List[MCQItem] = []
        previous_questions: List[str] = []
        
        for _ in range(count):
            mcq = heal_generation(RAGQuery(query=subject, k=k, level=level, language=language), previous_questions=previous_questions)
            items.append(mcq)
            previous_questions.append(mcq.question)
            
        return items
