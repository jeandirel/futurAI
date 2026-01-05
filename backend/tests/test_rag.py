import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.app.db.session import get_session
from backend.app.db.base import Base, Chunk, Document

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
    
    # Insert dummy data
    db = TestingSessionLocal()
    doc = Document(name="test_doc", path="test_path")
    db.add(doc)
    db.commit()
    
    chunk = Chunk(
        source="test_doc",
        position=0,
        text="Artificial Intelligence is a field of computer science.",
        embedding=[0.1]*1536, # Assuming 1536 dim, but pgvector might be different. 
        # Wait, pgvector type in sqlite might be issue. 
        # If using sqlite, we might not have vector type support unless mapped to something else or ignored.
        # The Chunk model likely uses Mapped[Vector].
        # In SQLite, we might need to mock the vector column or use a string if the model allows.
        # Let's check backend/app/db/base.py if possible, but for now assume it works or fails on vector type.
        # If it fails, we might need to patch search_chunks instead.
        doc_id=doc.id
    )
    # Actually, let's patch search_chunks to avoid vector DB issues in SQLite
    db.close()
    
    yield
    Base.metadata.drop_all(bind=engine)

from unittest.mock import patch
from backend.app.schemas.rag import RAGChunk

def test_rag_search_returns_chunks():
    # Patch search_chunks to avoid DB vector issues
    with patch("backend.app.api.rag.search_chunks") as mock_search:
        mock_search.return_value = [
            RAGChunk(source="test", position=0, text="AI is great")
        ]
        
        client = TestClient(app)
        resp = client.post("/rag/search", json={"query": "intelligence", "k": 2})
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "chunks" in data
        assert len(data["chunks"]) >= 1
        assert "text" in data["chunks"][0]

def test_rag_generate_returns_mcq():
    # Patch generate_mcq_from_rag to avoid DB/LLM issues
    from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language
    
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
    
    with patch("backend.app.api.rag.generate_mcq_from_rag") as mock_gen:
        mock_gen.return_value = mock_mcq
        
        client = TestClient(app)
        resp = client.post("/rag/generate", json={"query": "intelligence", "k": 2})
        assert resp.status_code == 200, resp.text
        mcq = resp.json()
        assert mcq["question"]
        assert mcq["answer"] in mcq["options"]

