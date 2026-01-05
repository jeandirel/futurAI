import pytest
from unittest.mock import MagicMock, patch
from backend.app.agents.generation import GenerationAgent
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language

def test_generation_agent_run():
    mock_db = MagicMock()
    agent = GenerationAgent(mock_db)
    
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
    
    with patch("backend.app.agents.generation.heal_generation", return_value=mock_mcq) as mock_heal:
        items = agent.run("subject", count=2, k=3)
        
        assert len(items) == 2
        assert mock_heal.call_count == 2
        # Verify arguments passed to heal_generation
        call_args = mock_heal.call_args[0][0]
        assert call_args.query == "subject"
        assert call_args.k == 3
