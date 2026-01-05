"""
Healing agent: détecte/relance en cas d'échec de génération.
"""

from backend.app.schemas.rag import RAGQuery
from backend.app.schemas.base import MCQItem
from backend.app.services.healing import heal_generation


class HealingAgent:
    def run(self, query: str, k: int = 3, max_attempts: int = 3) -> MCQItem:
        return heal_generation(RAGQuery(query=query, k=k), max_attempts=max_attempts)
