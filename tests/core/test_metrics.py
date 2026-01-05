import pytest
from backend.app.core.metrics import (
    rag_requests, rag_latency,
    llm_requests, llm_latency,
    healing_requests, healing_latency,
    jobs_created, jobs_completed, jobs_failed
)

def test_metrics_existence():
    # Verify all metrics are defined
    assert rag_requests
    assert rag_latency
    assert llm_requests
    assert llm_latency
    assert healing_requests
    assert healing_latency
    assert jobs_created
    assert jobs_completed
    assert jobs_failed

def test_metrics_increment():
    # Test incrementing a counter
    before = jobs_created._value.get()
    jobs_created.inc()
    after = jobs_created._value.get()
    assert after == before + 1

def test_metrics_labels():
    # Test labels on LLM requests
    llm_requests.labels(status="success", model="test").inc()
    # No assertion needed, just checking it doesn't raise
