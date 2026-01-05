import pytest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path
from backend.app.services.chunk_ingest import ingest_chunks
from backend.app.db.base import Document

def test_ingest_chunks_logic():
    # Mock data
    jsonl_content = '{"text": "foo", "source": "doc1", "position": 1}\n{"text": "bar", "source": "doc1", "position": 2}'
    
    # Mock Session
    mock_session = MagicMock()
    # Mock execute result for Document lookup (return None first to trigger creation)
    mock_session.execute.return_value.scalar_one_or_none.return_value = None
    
    # Mock SessionLocal to return our mock_session
    with patch("backend.app.services.chunk_ingest.SessionLocal", return_value=mock_session):
        # Mock file open
        with patch("pathlib.Path.open", mock_open(read_data=jsonl_content)):
            count = ingest_chunks(Path("dummy.jsonl"))
            
            assert count == 2
            # Check Document creation (once for doc1)
            assert mock_session.add.call_count >= 1 
            # Check bulk save (once at end)
            mock_session.bulk_save_objects.assert_called()
            # Check commit
            mock_session.commit.assert_called()
