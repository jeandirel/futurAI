import pytest
from unittest.mock import MagicMock, patch
from backend.app.agents.validation import ValidationAgent
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language

def test_validation_agent_run_basic():
    agent = ValidationAgent()
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
    
    with patch("backend.app.agents.validation.validate_mcq") as mock_val:
        items = agent.run([mock_mcq], llm_check=False)
        assert len(items) == 1
        mock_val.assert_called_once_with(mock_mcq)

def test_validation_agent_run_with_llm():
    agent = ValidationAgent()
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
    
    with patch("backend.app.agents.validation.validate_mcq"):
        with patch("backend.app.agents.validation.settings.use_llm", True):
            with patch("backend.app.agents.validation.generate_text_hf", return_value="OK") as mock_llm:
                items = agent.run([mock_mcq], llm_check=True)
                assert len(items) == 1
                mock_llm.assert_called_once()
                assert len(agent.last_reports) == 1
                assert agent.last_reports[0]["verdict"] == "OK"

def test_validation_agent_run_llm_fail():
    agent = ValidationAgent()
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
    
    with patch("backend.app.agents.validation.validate_mcq"):
        with patch("backend.app.agents.validation.settings.use_llm", True):
            with patch("backend.app.agents.validation.generate_text_hf", side_effect=Exception("Fail")):
                items = agent.run([mock_mcq], llm_check=True)
                assert len(items) == 1
                assert "indisponible" in agent.last_reports[0]["verdict"]
