import pytest
from unittest.mock import patch
from backend.app.agents.fairness import FairnessAgent
from backend.app.schemas.base import MCQItem, Language, Difficulty, Bloom, Solo

@pytest.fixture
def mock_mcq_fr():
    return MCQItem(
        question="Q_FR",
        options=["A", "B"],
        answer="A",
        bloom=Bloom.remember,
        solo=Solo.unistructural,
        difficulty=Difficulty.easy,
        language=Language.fr,
        topic="t"
    )

@pytest.fixture
def mock_mcq_en():
    return MCQItem(
        question="Q_EN",
        options=["A", "B"],
        answer="A",
        bloom=Bloom.remember,
        solo=Solo.unistructural,
        difficulty=Difficulty.easy,
        language=Language.en,
        topic="t"
    )

def test_fairness_agent_run(mock_mcq_fr, mock_mcq_en):
    agent = FairnessAgent()
    items = [mock_mcq_fr, mock_mcq_en]
    
    # Mock compute_metrics to return a dummy dict
    with patch("backend.app.agents.fairness.compute_metrics") as mock_metrics:
        mock_metrics.return_value = {"fr": 0.5, "en": 0.5}
        
        result = agent.run(items, group_field="language")
        
        assert result == {"fr": 0.5, "en": 0.5}
        mock_metrics.assert_called_once()
        call_args = mock_metrics.call_args
        assert len(call_args[0][0]) == 2 # payload length
        assert call_args[1]["group_field"] == "language"
