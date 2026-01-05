import pytest
from unittest.mock import patch, MagicMock
from backend.app.services.queue import enqueue_job, dequeue_job

def test_enqueue_job():
    with patch("backend.app.services.queue._client") as mock_client:
        mock_redis = MagicMock()
        mock_client.return_value = mock_redis
        
        enqueue_job("job-123")
        
        mock_redis.lpush.assert_called_once_with("jobs", "job-123")

def test_dequeue_job_block():
    with patch("backend.app.services.queue._client") as mock_client:
        mock_redis = MagicMock()
        mock_client.return_value = mock_redis
        # brpop returns (key, value) tuple
        mock_redis.brpop.return_value = ("jobs", "job-123")
        
        job_id = dequeue_job(block=True)
        
        assert job_id == "job-123"
        mock_redis.brpop.assert_called_once_with("jobs", timeout=5)

def test_dequeue_job_no_block():
    with patch("backend.app.services.queue._client") as mock_client:
        mock_redis = MagicMock()
        mock_client.return_value = mock_redis
        mock_redis.rpop.return_value = "job-123"
        
        job_id = dequeue_job(block=False)
        
        assert job_id == "job-123"
        mock_redis.rpop.assert_called_once_with("jobs")

def test_dequeue_job_empty():
    with patch("backend.app.services.queue._client") as mock_client:
        mock_redis = MagicMock()
        mock_client.return_value = mock_redis
        mock_redis.brpop.return_value = None
        
        job_id = dequeue_job(block=True)
        
        assert job_id is None
