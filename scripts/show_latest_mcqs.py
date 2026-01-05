import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.db.session import SessionLocal
from backend.app.db.base import Job, MCQ

def show_latest_mcqs():
    with SessionLocal() as db:
        # Get last completed job
        job = db.query(Job).filter(Job.status == "completed").order_by(Job.created_at.desc()).first()
        
        if not job:
            print("No completed jobs found.")
            return

        print(f"Job ID: {job.id}")
        print(f"Subject: {job.subject}")
        print(f"Level: {job.level}")
        print(f"Language: {job.language}")
        print(f"Created: {job.created_at}")
        print("-" * 40)
        
        mcqs = db.query(MCQ).filter(MCQ.job_id == job.id).all()
        
        for i, mcq in enumerate(mcqs, 1):
            print(f"Q{i}. {mcq.question}")
            print("Options:")
            for opt in mcq.options:
                print(f"  - {opt}")
            print(f"Réponse: {mcq.answer}")
            print(f"Bloom: {mcq.bloom} | SOLO: {mcq.solo} | Diff: {mcq.difficulty}")
            print("-" * 20)

if __name__ == "__main__":
    show_latest_mcqs()
