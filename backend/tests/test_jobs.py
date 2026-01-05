import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.app.db.session import get_session
from backend.app.db.base import Base

# Setup in-memory SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_job_returns_id_and_status(test_db):
    app.dependency_overrides[get_session] = override_get_session
    
    subject = f"test-{uuid.uuid4()}"
    client = TestClient(app)
    payload = {
        "subject": subject,
        "level": "test-level",
        "language": "fr",
        "count": 1,
    }
    
    # We also need to mock the background task or ensure it runs synchronously/is mocked
    # The job creation might trigger a background task.
    # For now, let's see if the API returns 200.
    
    resp = client.post("/jobs/generate", json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "job" in data
    assert data["job"]["status"] in ("completed", "failed", "pending")
    assert data["job"]["job_id"]

