"""
Fairness agent: calcule quelques indicateurs (acceptation/toxicité/healing) par groupe langue.
"""

from typing import List

from backend.app.schemas.base import MCQItem
from backend.app.services.evaluation import compute_metrics


class FairnessAgent:
    def run(self, items: List[MCQItem], group_field: str = "language") -> dict:
        # MCQItem -> dict pour reuse compute_metrics
        payload = [mcq.model_dump() for mcq in items]
        return compute_metrics(payload, group_field=group_field)
