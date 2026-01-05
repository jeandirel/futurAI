import pytest
from unittest.mock import patch
from backend.app.agents.feedback import FeedbackAgent
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language

def test_feedback_agent_run_basic():
    agent = FeedbackAgent()
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
    
    # Test without LLM (fallback)
    with patch("backend.app.agents.feedback.settings.use_llm", False):
        results = agent.run([mock_mcq])
        assert len(results) == 1
        assert "placeholder" in results[0]["explanation"]

def test_feedback_agent_run_with_llm():
    agent = FeedbackAgent()
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
    
    # Test with LLM mock
    with patch("backend.app.agents.feedback.settings.use_llm", True):
        with patch("backend.app.agents.feedback.generate_text_hf", return_value="Explication IA"):
            results = agent.run([mock_mcq])
            assert len(results) == 1
            assert results[0]["explanation"] == "Explication IA"

def test_feedback_agent_run_llm_fail():
    agent = FeedbackAgent()
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
    
    # Test with LLM failure -> fallback
    with patch("backend.app.agents.feedback.settings.use_llm", True):
        with patch("backend.app.agents.feedback.generate_text_hf", side_effect=Exception("Fail")):
            results = agent.run([mock_mcq])
            assert len(results) == 1
            assert "fallback" in results[0]["explanation"]
