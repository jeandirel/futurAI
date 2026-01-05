"""
Batch evaluation utilities for MCQ items: acceptance, latency, fairness, and F1 on Bloom/SOLO when reference labels are present.
"""

from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Tuple

from backend.app.schemas.base import Bloom, MCQItem, Solo
from backend.app.services.validation import validate_mcq

# Simple toxicity keyword list (placeholder, swap with a better classifier if available)
TOXIC_KEYWORDS = ["stupid", "idiot", "hate", "worthless", "kill"]


def load_mcq_file(path: Path) -> List[Dict[str, Any]]:
    """Load MCQ examples from JSONL or JSON."""
    records: List[Dict[str, Any]] = []
    if path.suffix.lower() == ".jsonl":
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            records.append(__import__("json").loads(line))
    else:
        import json

        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            records = data
        else:
            raise ValueError("JSON file must contain a list of items")
    return records


def _percentile(values: List[float], pct: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    k = (len(values) - 1) * pct
    f = int(k)
    c = min(f + 1, len(values) - 1)
    if f == c:
        return float(values[int(k)])
    d0 = values[f] * (c - k)
    d1 = values[c] * (k - f)
    return float(d0 + d1)


def _f1_score(truth: List[str], preds: List[str]) -> float:
    if not truth or not preds or len(truth) != len(preds):
        return 0.0
    tp = sum(1 for t, p in zip(truth, preds) if t == p)
    precision = tp / len(preds) if preds else 0.0
    recall = tp / len(truth) if truth else 0.0
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def _is_toxic(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in TOXIC_KEYWORDS)


def _healed_flag(raw: Dict[str, Any]) -> bool:
    # Accept several conventions: healed boolean, status string, or metadata flag
    if isinstance(raw.get("healed"), bool):
        return raw["healed"]
    status = str(raw.get("status") or "").lower()
    return status in {"healed", "fixed"}


def compute_metrics(items: List[Dict[str, Any]], group_field: str = "language") -> Dict[str, Any]:
    total = len(items)
    accepted = 0
    healed = 0
    latencies: List[float] = []
    bloom_true: List[str] = []
    bloom_pred: List[str] = []
    solo_true: List[str] = []
    solo_pred: List[str] = []
    group_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"count": 0, "accepted": 0, "heal": 0, "tox": 0})

    for raw in items:
        mcq = MCQItem(**raw)
        group = str(raw.get(group_field) or mcq.language)
        group_stats[group]["count"] += 1

        try:
            validate_mcq(mcq)
            accepted += 1
            group_stats[group]["accepted"] += 1
        except Exception:
            pass

        if _healed_flag(raw):
            healed += 1
            group_stats[group]["heal"] += 1

        lat = raw.get("latency_ms")
        if isinstance(lat, (int, float)):
            latencies.append(float(lat))

        if raw.get("bloom_true"):
            bloom_true.append(str(raw["bloom_true"]))
            bloom_pred.append(mcq.bloom.value if isinstance(mcq.bloom, Bloom) else str(mcq.bloom))
        if raw.get("solo_true"):
            solo_true.append(str(raw["solo_true"]))
            solo_pred.append(mcq.solo.value if isinstance(mcq.solo, Solo) else str(mcq.solo))

        texts = [mcq.question] + list(mcq.options)
        if any(_is_toxic(t) for t in texts):
            group_stats[group]["tox"] += 1

    fairness_groups = {}
    accept_rates: List[Tuple[str, float]] = []
    tox_rates: List[Tuple[str, float]] = []
    heal_rates: List[Tuple[str, float]] = []
    for g, stats in group_stats.items():
        cnt = stats["count"] or 1
        ar = stats["accepted"] / cnt
        tr = stats["tox"] / cnt
        hr = stats["heal"] / cnt
        fairness_groups[g] = {"accept_rate": ar, "toxicity_rate": tr, "healing_rate": hr, "count": stats["count"]}
        accept_rates.append((g, ar))
        tox_rates.append((g, tr))
        heal_rates.append((g, hr))

    def _spread(pairs: List[Tuple[str, float]]) -> float:
        if not pairs:
            return 0.0
        vals = [p[1] for p in pairs]
        return max(vals) - min(vals)

    metrics: Dict[str, Any] = {
        "total": total,
        "acceptance_rate": accepted / total if total else 0.0,
        "healing_rate": healed / total if total else 0.0,
        "latency_ms": None,
        "bloom_f1": _f1_score(bloom_true, bloom_pred) if bloom_true else None,
        "solo_f1": _f1_score(solo_true, solo_pred) if solo_true else None,
        "fairness": {
            "groups": fairness_groups,
            "acceptance_parity_diff": _spread(accept_rates),
            "toxicity_rate_diff": _spread(tox_rates),
            "healing_rate_diff": _spread(heal_rates),
        },
    }

    if latencies:
        metrics["latency_ms"] = {
            "p50": _percentile(latencies, 0.5),
            "p95": _percentile(latencies, 0.95),
            "avg": mean(latencies),
        }
    return metrics
