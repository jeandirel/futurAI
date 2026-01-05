import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from backend.app.agents.archivist import ArchivistAgent

def test_archivist_ingest_jsonl():
    agent = ArchivistAgent()
    path = Path("test.jsonl")
    
    with patch("backend.app.services.chunk_ingest.ingest_chunks") as mock_ingest:
        mock_ingest.return_value = 10
        
        result = agent.ingest([path])
        
        assert result["results"]["test.jsonl"] == "ingested_10_chunks"
        mock_ingest.assert_called_once_with(path)

def test_archivist_ingest_skipped():
    agent = ArchivistAgent()
    path = Path("test.txt")
    
    result = agent.ingest([path])
    
    assert result["results"]["test.txt"] == "skipped_not_jsonl"
