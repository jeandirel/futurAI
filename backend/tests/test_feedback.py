import pytest
from unittest.mock import patch, MagicMock
from backend.app.agents.feedback import FeedbackAgent
from backend.app.schemas.base import MCQItem, Language, Difficulty, Bloom, Solo

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
        topic="t"
    )

def test_feedback_agent_run(mock_mcq):
    agent = FeedbackAgent()
    
    with patch("backend.app.agents.feedback.generate_text_hf") as mock_llm:
        mock_llm.return_value = "Explanation from LLM"
        
        results = agent.run([mock_mcq])
        
        assert len(results) == 1
        assert results[0]["explanation"] == "Explanation from LLM"
        assert results[0]["question"] == "Q?"
