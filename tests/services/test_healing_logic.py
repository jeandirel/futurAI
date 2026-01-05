import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from backend.app.services.healing import heal_generation
from backend.app.schemas.rag import RAGQuery
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language

@pytest.fixture
def mock_mcq():
    return MCQItem(
        question="Q?",
        options=["A", "B"],
        answer="A",
        bloom=Bloom.remember,
        solo=Solo.unistructural,
        difficulty=Difficulty.easy,
        language=Language.fr,
        topic="t",
        source="s"
    )

def test_heal_generation_success_first_try(mock_mcq):
    payload = RAGQuery(query="test", k=1)
    
    with patch("backend.app.services.healing.SessionLocal"):
        with patch("backend.app.services.healing.generate_mcq_from_rag", return_value=mock_mcq) as mock_gen:
            with patch("backend.app.services.healing.validate_mcq") as mock_val:
                result = heal_generation(payload)
                assert result == mock_mcq
                mock_gen.assert_called_once()
                mock_val.assert_called_once()

def test_heal_generation_retry_success(mock_mcq):
    payload = RAGQuery(query="test", k=1)
    
    with patch("backend.app.services.healing.SessionLocal"):
        # First call raises exception, second returns valid MCQ
        with patch("backend.app.services.healing.generate_mcq_from_rag", side_effect=[Exception("Fail"), mock_mcq]) as mock_gen:
            with patch("backend.app.services.healing.validate_mcq") as mock_val:
                result = heal_generation(payload)
                assert result == mock_mcq
                assert mock_gen.call_count == 2
                # validate called only on success (or if we validate inside loop, checking logic)
                # In healing.py: validate_mcq is called after generation.
                # 1st attempt: generate fails -> catch -> loop
                # 2nd attempt: generate succeeds -> validate succeeds -> return
                assert mock_val.call_count == 1

def test_heal_generation_max_attempts_fail(mock_mcq):
    payload = RAGQuery(query="test", k=1)
    
    with patch("backend.app.services.healing.SessionLocal"):
        with patch("backend.app.services.healing.generate_mcq_from_rag", return_value=mock_mcq):
            # Always fail validation
            with patch("backend.app.services.healing.validate_mcq", side_effect=ValueError("Invalid")):
                with pytest.raises(HTTPException) as exc:
                    heal_generation(payload, max_attempts=2)
                assert exc.value.status_code == 500
                assert "Healing failed" in exc.value.detail
