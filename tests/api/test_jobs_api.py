import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.app.main import app
from backend.app.db.base import Job
from backend.app.schemas.job import JobStatus
from datetime import datetime

client = TestClient(app)

def test_create_job_success():
    payload = {
        "subject": "Test Subject",
        "level": "easy",
        "language": "fr",
        "count": 5
    }
    
    with patch("backend.app.api.jobs.enqueue_job") as mock_enqueue:
        # We need to mock the DB session commit/refresh/add
        # But since we use Depends(get_session), it's easier to use a real DB session 
        # or mock the dependency override if we want pure unit test.
        # For simplicity in this project context, we often rely on the fact that 
        # tests might use a test DB or we mock the DB interactions if possible.
        # Given the complexity of mocking SQLAlchemy session in simple tests, 
        # we'll assume the test environment allows DB access OR we mock the router logic partially.
        # However, mocking the router function is not testing the router.
        
        # Let's mock the DB dependency if we want to avoid real DB
        # But here we will just mock the enqueue_job to avoid Redis connection
        
        response = client.post("/jobs/generate", json=payload)
        
        # If DB is not set up for tests, this might fail. 
        # Assuming the project has a test DB setup or we accept integration test nature.
        # If it fails, we'll see 500.
        
        assert response.status_code == 200
        data = response.json()
        assert data["job"]["status"] == "pending"
        assert "job_id" in data["job"]
        mock_enqueue.assert_called_once()

def test_get_job_status():
    # We need a job in DB. 
    # Create one via API first (mocking enqueue)
    with patch("backend.app.api.jobs.enqueue_job"):
        create_resp = client.post("/jobs/generate", json={
            "subject": "Status Test",
            "level": "medium",
            "language": "en",
            "count": 1
        })
        job_id = create_resp.json()["job"]["job_id"]
        
    response = client.get(f"/jobs/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == job_id
    assert data["status"] == "pending"

def test_list_jobs():
    response = client.get("/jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
