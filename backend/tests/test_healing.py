from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language

def test_heal_generate_returns_mcq():
    mock_mcq = MCQItem(
        question="Q?",
        options=["A", "B"],
        answer="A",
        bloom=Bloom.remember,
        solo=Solo.unistructural,
        difficulty=Difficulty.easy,
        language=Language.fr,
        topic="t"
    )
    
    with patch("backend.app.api.rag.heal_generation") as mock_heal:
        mock_heal.return_value = mock_mcq
        
        client = TestClient(app)
        resp = client.post("/rag/generate/heal", json={"query": "intelligence", "k": 2})
        
        assert resp.status_code == 200, resp.text
        mcq = resp.json()
        assert mcq["answer"] in mcq["options"]
        assert len(set(mcq["options"])) == len(mcq["options"])

