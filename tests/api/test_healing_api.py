import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from backend.app.main import app
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language

client = TestClient(app)

def test_rag_generate_heal_endpoint():
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
    
    with patch("backend.app.api.rag.heal_generation", return_value=mock_mcq) as mock_heal:
        response = client.post("/rag/generate/heal", json={"query": "test", "k": 3})
        assert response.status_code == 200
        data = response.json()
        assert data["question"] == "Q?"
        mock_heal.assert_called_once()
