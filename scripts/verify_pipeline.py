import sys
import os
from unittest.mock import MagicMock, patch

# 1. Mock critical dependencies that might be missing or require Docker
# Mock pgvector before it's imported by backend.app.db.base
mock_pgvector = MagicMock()
sys.modules["pgvector"] = mock_pgvector
sys.modules["pgvector.sqlalchemy"] = mock_pgvector

# Mock Redis
sys.modules["redis"] = MagicMock()

# Set environment variables to avoid validation errors in Settings
os.environ["POSTGRES_DSN"] = "postgresql://mock:mock@localhost:5432/mock"
os.environ["REDIS_URL"] = "redis://mock:6379/0"
os.environ["HF_API_TOKEN"] = "mock_token"

# 2. Import backend modules
# We need to patch SessionLocal in healing.py because it creates its own session
from backend.app.services import healing
from backend.app.services import rag
from backend.app.schemas.rag import RAGChunk
from backend.app.services.agent_orchestrator import AgentOrchestrator
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language

# 3. Define Mocks
def mock_search_chunks(query, k, db):
    print(f"[Mock] Searching chunks for query: {query}")
    return [
        RAGChunk(
            source="Mock Source",
            position=1,
            text=f"This is a mock context for {query}. It contains relevant information."
        )
    ]

# Mock DB Session
mock_db_session = MagicMock()
mock_session_cls = MagicMock(return_value=mock_db_session)
# Context manager support for SessionLocal()
mock_session_cls.return_value.__enter__.return_value = mock_db_session

# 4. Patch and Run
def run_verification():
    print("Starting Pipeline Verification...")

    # Patch search_chunks to avoid DB access
    with patch("backend.app.services.rag.search_chunks", side_effect=mock_search_chunks):
        # Patch SessionLocal in healing.py
        with patch("backend.app.services.healing.SessionLocal", side_effect=mock_session_cls):
            
            # Initialize Orchestrator (pass mock DB)
            orchestrator = AgentOrchestrator(db=mock_db_session)
            
            subject = "Artificial Intelligence"
            print(f"Generating pipeline for subject: {subject}")
            
            try:
                # Run the pipeline
                # We disable validation_llm to avoid external API calls if not configured
                result = orchestrator.generate_pipeline(
                    subject=subject,
                    count=1,
                    k=3,
                    compute_feedback=True,
                    compute_fairness=True,
                    validation_llm=False 
                )
                
                print("\n--- Generation Success ---")
                items = result["items"]
                print(f"Generated {len(items)} items.")
                for idx, item in enumerate(items):
                    print(f"\nItem {idx+1}:")
                    print(f"Question: {item.question}")
                    print(f"Options: {item.options}")
                    print(f"Answer: {item.answer}")
                    print(f"Source: {item.source}")
                
                print("\n--- Feedback ---")
                print(result.get("feedback"))
                
                print("\n--- Fairness ---")
                print(result.get("fairness"))
                
                print("\nVerification PASSED.")
                
            except Exception as e:
                print(f"\nVerification FAILED with error: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    run_verification()
