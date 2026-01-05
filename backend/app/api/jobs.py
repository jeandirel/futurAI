import structlog
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db.base import Job, MCQ
from ..db.session import get_session
from ..schemas.base import MCQItem
from ..schemas.job import (
    GenerateRequest,
    GenerateResponse,
    JobDetail,
    JobInfo,
    JobStatus,
    JobSummary,
)
from ..services.agent_orchestrator import AgentOrchestrator
from ..services.queue import enqueue_job
from ..core.metrics import jobs_created, jobs_completed, jobs_failed

logger = structlog.get_logger(__name__)

router = APIRouter()
logger = structlog.get_logger(__name__)


@router.post("/generate", response_model=GenerateResponse, summary="Create a generation job (async)")
def create_job(payload: GenerateRequest, db: Session = Depends(get_session)) -> GenerateResponse:
    job = Job(
        subject=payload.subject,
        level=payload.level,
        language=payload.language.value,
        count=payload.count,
        status=JobStatus.pending.value,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    try:
        jobs_created.inc()
        enqueue_job(str(job.id))
        logger.info("job_created_enqueued", job_id=str(job.id))
    except Exception as exc:  # noqa: BLE001
        logger.warning("job_enqueue_failed", job_id=str(job.id), error=str(exc))
        job.status = JobStatus.failed.value
        job.message = f"Enqueue failed: {str(exc)}"
        db.add(job)
        db.commit()
        jobs_failed.inc()
        
    info = JobInfo(job_id=str(job.id), status=JobStatus(job.status), message=job.message)
    return GenerateResponse(job=info, items=None)


@router.get("/jobs/{job_id}", response_model=JobInfo, summary="Get job status (stub)")
def get_job(job_id: str, db: Session = Depends(get_session)) -> JobInfo:
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobInfo(job_id=str(job.id), status=JobStatus(job.status), message=job.message)


@router.get("", response_model=list[JobSummary], summary="List jobs with filters")
def list_jobs(
    db: Session = Depends(get_session),
    status: JobStatus | None = Query(default=None),
    language: str | None = Query(default=None),
    level: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[JobSummary]:
    q = db.query(Job)
    if status:
        q = q.filter(Job.status == status.value)
    if language:
        q = q.filter(Job.language == language)
    if level:
        q = q.filter(Job.level == level)
    rows = q.order_by(Job.created_at.desc()).offset(offset).limit(limit).all()
    return [
        JobSummary(
            job_id=str(r.id),
            status=JobStatus(r.status),
            subject=r.subject,
            level=r.level,
            language=r.language,
            count=r.count,
            message=r.message,
            created_at=r.created_at.isoformat() + "Z" if r.created_at else None,
        )
        for r in rows
    ]


@router.get("/{job_id}", response_model=JobDetail, summary="Get job detail with MCQ items")
def get_job_detail(job_id: str, db: Session = Depends(get_session)) -> JobDetail:
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    items = [
        MCQItem(
            question=m.question,
            options=m.options,
            answer=m.answer,
            bloom=m.bloom,
            solo=m.solo,
            difficulty=m.difficulty,
            language=m.language,
            topic=m.topic,
            source=m.source,
            notes=m.notes,
        )
        for m in job.mcq_items
    ]
    return JobDetail(
        job_id=str(job.id),
        status=JobStatus(job.status),
        subject=job.subject,
        level=job.level,
        language=job.language,
        count=job.count,
        message=job.message,
        created_at=job.created_at.isoformat() + "Z" if job.created_at else None,
        items=items or None,
    )
