import pytest
from unittest.mock import MagicMock, patch
from backend.app.agents.generation import GenerationAgent
from backend.app.schemas.base import MCQItem, Language, Difficulty, Bloom, Solo

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_mcq():
    return MCQItem(
        question="What is AI?",
        options=["Artificial Intelligence", "Apple Inc", "An Idea", "All In"],
        answer="Artificial Intelligence",
        bloom=Bloom.remember,
        solo=Solo.unistructural,
        difficulty=Difficulty.easy,
        language=Language.en,
        topic="AI"
    )

def test_generation_agent_run(mock_db, mock_mcq):
    agent = GenerationAgent(mock_db)
    
    with patch("backend.app.agents.generation.heal_generation") as mock_heal:
        mock_heal.return_value = mock_mcq
        
        items = agent.run(subject="AI", count=2, k=3)
        
        assert len(items) == 2
        assert items[0] == mock_mcq
        assert items[1] == mock_mcq
        assert mock_heal.call_count == 2
        
        # Verify call args
        call_args = mock_heal.call_args
        rag_query = call_args[0][0]
        assert rag_query.query == "AI"
        assert rag_query.k == 3
