import pytest
from unittest.mock import MagicMock, patch
from backend.app.services.rag import search_chunks, _redact_pii

def test_redact_pii():
    text = "Contact me at test@example.com or +33 6 12 34 56 78."
    redacted = _redact_pii(text)
    assert "[email]" in redacted
    assert "[phone]" in redacted
    assert "test@example.com" not in redacted

def test_search_chunks():
    mock_session = MagicMock()
    # Mock DB result
    mock_row = MagicMock()
    mock_row.source = "doc1"
    mock_row.position = 1
    mock_row.text = "Sensitive info: test@test.com"
    mock_session.execute.return_value.fetchall.return_value = [mock_row]
    
    results = search_chunks("query", 1, mock_session)
    
    assert len(results) == 1
    assert results[0].source == "doc1"
    assert "[email]" in results[0].text # Verify redaction happens
