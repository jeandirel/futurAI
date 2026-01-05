import pytest
from unittest.mock import MagicMock, patch
from backend.app.services.healing import heal_generation
from backend.app.schemas.rag import RAGQuery
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language
from fastapi import HTTPException

def test_heal_generation_success_first_try():
    mock_mcq = MCQItem(
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
    
    with patch("backend.app.services.healing.generate_mcq_from_rag", return_value=mock_mcq):
        with patch("backend.app.services.healing.validate_mcq"): # No error
            with patch("backend.app.services.healing.SessionLocal"):
                payload = RAGQuery(query="test")
                result = heal_generation(payload)
                assert result == mock_mcq

def test_heal_generation_retry_success():
    mock_mcq = MCQItem(
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
    
    # First call raises Exception (validation fail), second succeeds
    with patch("backend.app.services.healing.generate_mcq_from_rag", return_value=mock_mcq):
        with patch("backend.app.services.healing.validate_mcq", side_effect=[Exception("Fail"), None]):
             with patch("backend.app.services.healing.SessionLocal"):
                payload = RAGQuery(query="test")
                result = heal_generation(payload, max_attempts=2)
                assert result == mock_mcq

def test_heal_generation_fail_max_attempts():
    with patch("backend.app.services.healing.generate_mcq_from_rag"):
        with patch("backend.app.services.healing.validate_mcq", side_effect=Exception("Fail")):
             with patch("backend.app.services.healing.SessionLocal"):
                payload = RAGQuery(query="test")
                with pytest.raises(HTTPException, match="Healing failed"):
                    heal_generation(payload, max_attempts=2)
