import pytest
from unittest.mock import MagicMock, patch
from backend.app.services.generator import generate_mcq_from_rag
from backend.app.schemas.rag import RAGChunk

def test_generate_mcq_no_chunks():
    mock_db = MagicMock()
    with patch("backend.app.services.generator.search_chunks", return_value=[]):
        # Should raise ValueError if no chunks and no LLM fallback configured/mocked to succeed immediately without chunks
        # But looking at code: if not chunks -> logger.warning -> if settings.use_llm -> generate... else raise ValueError
        
        # Case 1: No LLM, No Chunks -> Error
        with patch("backend.app.services.generator.settings.use_llm", False):
            with pytest.raises(ValueError, match="No chunks found"):
                generate_mcq_from_rag("query", mock_db)

def test_generate_mcq_placeholder_fallback():
    mock_db = MagicMock()
    mock_chunk = RAGChunk(source="s", position=0, text="content")
    
    with patch("backend.app.services.generator.search_chunks", return_value=[mock_chunk]):
        with patch("backend.app.services.generator.settings.use_llm", False):
            # Should use placeholder logic
            mcq = generate_mcq_from_rag("query", mock_db)
            assert mcq.source == "s"
            assert "placeholder" in mcq.notes or "Genere a partir du top-k RAG" in mcq.notes
