import time
import structlog
from sqlalchemy.orm import Session

from backend.app.db.session import SessionLocal
from backend.app.db.base import Job, MCQ
from backend.app.schemas.job import JobStatus
from backend.app.services.queue import dequeue_job
from backend.app.services.agent_orchestrator import AgentOrchestrator
from backend.app.core.metrics import jobs_completed, jobs_failed
from backend.app.core.logging import configure_logging

logger = structlog.get_logger(__name__)

def process_job(job_id: str, db: Session):
    job = db.get(Job, job_id)
    if not job:
        logger.error("worker_job_not_found", job_id=job_id)
        return

    logger.info("worker_processing_job", job_id=job_id)
    job.status = JobStatus.running.value
    db.commit()

    try:
        orch = AgentOrchestrator(db)
        # Note: We might want to pass more params from the job if we stored them, 
        # but for now we rely on what's in the job record or defaults.
        # The original code in jobs.py used payload.subject, payload.count etc.
        # We need to ensure we have access to these. 
        # The Job model has subject, level, language, count.
        
        result = orch.generate_pipeline(
            subject=job.subject,
            count=job.count,
            k=3, # Default
            level=job.level,
            language=job.language,
            compute_feedback=False, # Default
            compute_fairness=False, # Default
        )
        
        items = result["items"]
        for mcq in items:
            mcq_row = MCQ(
                job_id=job.id,
                question=mcq.question,
                options=mcq.options,
                answer=mcq.answer,
                bloom=mcq.bloom,
                solo=mcq.solo,
                difficulty=mcq.difficulty,
                language=mcq.language,
                topic=mcq.topic,
                source=mcq.source,
                notes=mcq.notes,
            )
            db.add(mcq_row)
            
        job.status = JobStatus.completed.value
        job.message = f"{len(items)} items generated"
        db.add(job)
        db.commit()
        jobs_completed.inc()
        logger.info("worker_job_completed", job_id=job_id, items=len(items))
        
    except Exception as exc:
        logger.exception("worker_job_failed", job_id=job_id, error=str(exc))
        job.status = JobStatus.failed.value
        job.message = str(exc)
        db.add(job)
        db.commit()
        jobs_failed.inc()

def run_worker():
    configure_logging()
    logger.info("worker_started")
    while True:
        try:
            job_id = dequeue_job(block=True, timeout=5)
            if job_id:
                with SessionLocal() as db:
                    process_job(job_id, db)
        except Exception as exc:
            logger.error("worker_loop_error", error=str(exc))
            time.sleep(1)

if __name__ == "__main__":
    run_worker()
