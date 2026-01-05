import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.schemas.rag import RAGChunk
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language

client = TestClient(app)

def test_rag_search_api():
    with patch("backend.app.api.rag.search_chunks") as mock_search:
        mock_search.return_value = [
            RAGChunk(source="doc1", position=0, text="content")
        ]
        
        resp = client.post("/rag/search", json={"query": "test", "k": 1})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["chunks"]) == 1
        assert data["chunks"][0]["source"] == "doc1"

def test_rag_generate_api():
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
    
    with patch("backend.app.api.rag.generate_mcq_from_rag") as mock_gen:
        mock_gen.return_value = mock_mcq
        
        resp = client.post("/rag/generate", json={"query": "test", "k": 1})
        assert resp.status_code == 200
        data = resp.json()
        assert data["question"] == "Q?"

def test_rag_generate_heal_api():
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
    
    with patch("backend.app.api.rag.heal_generation") as mock_heal:
        mock_heal.return_value = mock_mcq
        
        resp = client.post("/rag/generate/heal", json={"query": "test", "k": 1})
        assert resp.status_code == 200
        data = resp.json()
        assert data["question"] == "Q?"
