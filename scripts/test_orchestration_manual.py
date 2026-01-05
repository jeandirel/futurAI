import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Add project root to path
sys.path.append(str(Path(__file__).parents[1]))

from backend.app.main import app
from backend.app.db.session import SessionLocal
from backend.app.worker import process_job
from backend.app.db.base import Job

client = TestClient(app)

def test_manual():
    print("=== Test Manuel : Orchestration (API + Worker) ===\n")
    
    # 1. API Call (Create Job)
    print("1. Appel API : Création d'un job de génération...")
    payload = {
        "subject": "L'histoire de l'informatique",
        "level": "débutant",
        "language": "fr",
        "count": 1
    }
    
    # We mock enqueue_job to avoid needing real Redis
    with patch("backend.app.api.jobs.enqueue_job") as mock_enqueue:
        response = client.post("/jobs/generate", json=payload)
        
        if response.status_code != 200:
            print(f"❌ Erreur API : {response.text}")
            return
            
        data = response.json()
        job_id = data["job"]["job_id"]
        print(f"✅ Job créé avec succès. ID: {job_id}")
        print(f"   Statut initial: {data['job']['status']}")
        
        # Verify enqueue was called
        mock_enqueue.assert_called_once_with(job_id)
        print("   (Job ajouté à la file d'attente simulée)")

    # 2. Worker Simulation (Process Job)
    print("\n2. Simulation du Worker (Traitement du job)...")
    print("   Le worker récupère le job et lance la génération...")
    
    # We mock the Orchestrator to avoid calling real LLMs (optional, but faster/safer)
    # OR we let it run for real if we want to test the full chain including LLM.
    # Let's let it run for real (or mock if no API key). 
    # Assuming user has OpenRouter key configured from Phase 4.
    
    try:
        with SessionLocal() as db:
            # Manually trigger the worker logic
            process_job(job_id, db)
            
            # 3. Verification
            print("\n3. Vérification du résultat...")
            db.expire_all() # Refresh
            job = db.get(Job, job_id)
            
            print(f"   Statut final: {job.status}")
            print(f"   Message: {job.message}")
            if job.status == "completed":
                print(f"   Items générés: {len(job.mcq_items)}")
                if job.mcq_items:
                    print(f"   Exemple: {job.mcq_items[0].question}")
                print("✅ SUCCÈS : Le cycle complet API -> Worker -> DB a fonctionné.")
            else:
                print("❌ ÉCHEC : Le job n'est pas terminé.")
                
    except Exception as e:
        print(f"❌ Erreur durant le traitement : {e}")

if __name__ == "__main__":
    test_manual()
