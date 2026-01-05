import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add project root to path to import frontend.app
ROOT = Path(__file__).parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# Mock streamlit before importing frontend.app
mock_st = MagicMock()
# Configure cache_data to be a pass-through decorator
# usage: @st.cache_data(ttl=...) -> returns decorator -> returns func
def mock_cache_data(*args, **kwargs):
    def decorator(f):
        return f
    return decorator
mock_st.cache_data = mock_cache_data
sys.modules["streamlit"] = mock_st

from frontend.app import load_jobs, load_job_detail, load_metrics

def test_load_jobs_success():
    mock_resp = MagicMock()
    mock_resp.json.return_value = [{"job_id": "1", "status": "completed"}]
    mock_resp.raise_for_status = MagicMock()
    
    with patch("requests.get", return_value=mock_resp) as mock_get:
        jobs = load_jobs("http://api", status=None)
        assert len(jobs) == 1
        assert jobs[0]["job_id"] == "1"
        mock_get.assert_called_with("http://api/jobs", params=None, timeout=30)

def test_load_jobs_with_status():
    mock_resp = MagicMock()
    mock_resp.json.return_value = []
    
    with patch("requests.get", return_value=mock_resp) as mock_get:
        load_jobs("http://api", status="failed")
        mock_get.assert_called_with("http://api/jobs", params={"status": "failed"}, timeout=30)

def test_load_job_detail():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"job_id": "1", "items": []}
    
    with patch("requests.get", return_value=mock_resp) as mock_get:
        detail = load_job_detail("http://api", "1")
        assert detail["job_id"] == "1"
        mock_get.assert_called_with("http://api/jobs/1", params=None, timeout=30)

def test_load_metrics():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"jobs": {"total": 10}}
    
    with patch("requests.get", return_value=mock_resp) as mock_get:
        metrics = load_metrics("http://api")
        assert metrics["jobs"]["total"] == 10
        mock_get.assert_called_with("http://api/metrics", params=None, timeout=30)
