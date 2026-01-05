"""
Feedback agent: génère des explications et vérifie la tonalité (placeholder).
"""

from typing import List

from backend.app.schemas.base import MCQItem
from backend.app.core.settings import settings
from backend.app.services.llm import generate_text


class FeedbackAgent:
    def run(self, items: List[MCQItem]) -> List[dict]:
        results = []
        for mcq in items:
            explanation = "Explication automatique (placeholder)."
            if settings.use_llm:
                prompt = (
                    "Explique en quelques lignes la réponse correcte de ce QCM, en "
                    "restant factuel et non toxique. Fourni en français.\n"
                    f"Question: {mcq.question}\n"
                    f"Options: {mcq.options}\n"
                    f"Réponse correcte: {mcq.answer}\n"
                )
                try:
                    explanation = generate_text(prompt)
                except Exception:
                    explanation = "Explication automatique (fallback)."
            results.append(
                {
                    "question": mcq.question,
                    "answer": mcq.answer,
                    "explanation": explanation,
                    "language": mcq.language,
                }
            )
        return results
