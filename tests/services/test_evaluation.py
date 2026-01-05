import pytest
from backend.app.services.evaluation import compute_metrics, _f1_score, _percentile

def test_f1_score():
    assert _f1_score(["A", "B"], ["A", "B"]) == 1.0
    assert _f1_score(["A", "B"], ["A", "C"]) == 0.5
    assert _f1_score(["A"], ["B"]) == 0.0
    assert _f1_score([], []) == 0.0

def test_percentile():
    vals = [10, 20, 30, 40, 50]
    assert _percentile(vals, 0.5) == 30.0
    assert _percentile(vals, 0.0) == 10.0
    assert _percentile(vals, 1.0) == 50.0

def test_compute_metrics_basic():
    items = [
        {
            "question": "Q1", "options": ["A", "B"], "answer": "A", 
            "bloom": "remember", "solo": "unistructural", "difficulty": "easy",
            "language": "fr", "topic": "t", "source": "s"
        },
        {
            "question": "Q2", "options": ["A", "B"], "answer": "B", 
            "bloom": "remember", "solo": "unistructural", "difficulty": "easy",
            "language": "en", "topic": "t", "source": "s"
        }
    ]
    
    metrics = compute_metrics(items, group_field="language")
    assert metrics["total"] == 2
    assert metrics["acceptance_rate"] == 1.0 # Both valid
    assert "fr" in metrics["fairness"]["groups"]
    assert "en" in metrics["fairness"]["groups"]

def test_compute_metrics_toxicity():
    items = [
        {
            "question": "You are stupid", "options": ["A", "B"], "answer": "A", 
            "bloom": "remember", "solo": "unistructural", "difficulty": "easy",
            "language": "en", "topic": "t", "source": "s"
        }
    ]
    # Assuming TOXIC_KEYWORDS includes "stupid"
    metrics = compute_metrics(items)
    assert metrics["fairness"]["groups"]["en"]["toxicity_rate"] == 1.0

def test_compute_metrics_healing():
    items = [
        {
            "question": "Q1", "options": ["A", "B"], "answer": "A", 
            "bloom": "remember", "solo": "unistructural", "difficulty": "easy",
            "language": "fr", "topic": "t", "source": "s",
            "healed": True
        }
    ]
    metrics = compute_metrics(items)
    assert metrics["healing_rate"] == 1.0
