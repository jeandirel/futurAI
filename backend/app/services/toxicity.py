"""
Toxicity checker with Hugging Face Inference API (text-classification).
Falls back to a simple keyword list if API fails or is disabled.
"""

import os
from typing import List

import requests
import structlog

from backend.app.core.metrics import toxicity_blocked, toxicity_checks
from backend.app.core.settings import settings

logger = structlog.get_logger(__name__)

TOXICITY_KEYWORDS = ["stupid", "idiot", "hate", "racist", "sexist", "kill", "terrorist"]


def _toxic_keyword(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in TOXICITY_KEYWORDS)


def _hf_headers() -> dict:
    token = settings.hf_api_token or os.environ.get("HF_API_TOKEN")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def is_toxic(text: str) -> bool:
    """Return True if toxic, using HF model when enabled; otherwise keyword check."""
    toxicity_checks.inc()
    if not settings.use_toxicity:
        return _toxic_keyword(text)

    model_id = settings.toxicity_model_id or "unitary/unbiased-toxic-roberta"
    base = settings.toxicity_api_base.rstrip("/")
    try:
        resp = requests.post(
            f"{base}/models/{model_id}",
            headers=_hf_headers(),
            json={"inputs": text},
            timeout=settings.hf_timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        # data may be list of dicts: [[{label, score}...]] or similar
        scores: List[dict] = []
        if isinstance(data, list):
            if data and isinstance(data[0], list):
                scores = data[0]
            elif data and isinstance(data[0], dict):
                scores = data
        tox_score = 0.0
        for entry in scores:
            label = str(entry.get("label", "")).lower()
            score = float(entry.get("score", 0.0))
            if "toxic" in label or "hate" in label or "insult" in label:
                tox_score = max(tox_score, score)
        toxic = tox_score >= settings.toxicity_threshold
        if toxic:
            toxicity_blocked.inc()
        return toxic
    except Exception as exc:  # noqa: BLE001
        logger.warning("toxicity_fallback", error=str(exc))
        toxic = _toxic_keyword(text)
        if toxic:
            toxicity_blocked.inc()
        return toxic
