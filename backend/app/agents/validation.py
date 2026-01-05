"""
Validation agent: applique les règles de structure/PII/toxicité.
"""

from typing import List

from backend.app.schemas.base import MCQItem
from backend.app.services.validation import validate_mcq
from backend.app.core.settings import settings
from backend.app.services.llm import generate_text


class ValidationAgent:
    def __init__(self) -> None:
        self.last_reports: List[dict] = []

    def run(self, items: List[MCQItem], llm_check: bool = False) -> List[MCQItem]:
        self.last_reports = []
        for mcq in items:
            validate_mcq(mcq)
            if llm_check and settings.use_llm:
                prompt = (
                    "Vérifie rapidement la cohérence Bloom/SOLO/difficulté du QCM ci-dessous. "
                    "Réponds par une phrase courte, en français.\n"
                    f"Question: {mcq.question}\n"
                    f"Options: {mcq.options}\n"
                    f"Réponse: {mcq.answer}\n"
                    f"Bloom: {mcq.bloom}, SOLO: {mcq.solo}, Difficulté: {mcq.difficulty}\n"
                )
                try:
                    verdict = generate_text(prompt)
                except Exception as exc:  # noqa: BLE001
                    verdict = f"Check LLM indisponible ({exc})"
                self.last_reports.append(
                    {
                        "question": mcq.question,
                        "verdict": verdict,
                    }
                )
        return items
