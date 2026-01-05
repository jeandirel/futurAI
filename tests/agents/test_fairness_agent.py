import pytest
from unittest.mock import patch
from backend.app.agents.fairness import FairnessAgent
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language

def test_fairness_agent_run():
    agent = FairnessAgent()
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
    
    # Verify it delegates to compute_metrics
    with patch("backend.app.agents.fairness.compute_metrics", return_value={"mock": "metrics"}) as mock_compute:
        res = agent.run([mock_mcq], group_field="language")
        assert res == {"mock": "metrics"}
        mock_compute.assert_called_once()
        # Check that payload is list of dicts
        args, _ = mock_compute.call_args
        assert isinstance(args[0], list)
        assert args[0][0]["question"] == "Q?"
