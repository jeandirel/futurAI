import datetime
from fastapi import APIRouter, Depends, Response
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from ..core.metrics import CONTENT_TYPE_LATEST, generate_latest
from ..db.base import Job, MCQ
from ..db.session import get_session

router = APIRouter()


@router.get("", summary="Metrics snapshot (JSON)")
def metrics(db: Session = Depends(get_session)) -> dict:
    total_jobs = db.query(func.count(Job.id)).scalar() or 0
    completed = db.query(func.count(Job.id)).filter(Job.status == "completed").scalar() or 0
    failed = db.query(func.count(Job.id)).filter(Job.status == "failed").scalar() or 0
    pending = db.query(func.count(Job.id)).filter(Job.status == "pending").scalar() or 0
    running = db.query(func.count(Job.id)).filter(Job.status == "running").scalar() or 0

    total_mcq = db.query(func.count(MCQ.id)).scalar() or 0
    latest_job = (
        db.query(Job.created_at)
        .order_by(Job.created_at.desc())
        .limit(1)
        .scalar()
    )

    # Latence moyenne stockée si présent dans fairness_metrics ou messages : non disponible => placeholder None
    # On peut néanmoins approximer la volumétrie par job
    avg_mcq_per_job = None
    if total_jobs:
        avg_mcq_per_job = total_mcq / total_jobs

    snapshot = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "jobs": {
            "total": total_jobs,
            "completed": completed,
            "failed": failed,
            "pending": pending,
            "running": running,
            "avg_mcq_per_job": avg_mcq_per_job,
            "latest_created_at": latest_job.isoformat() + "Z" if latest_job else None,
        },
        "mcq": {
            "total": total_mcq,
        },
    }
    return snapshot


@router.get("/prom", summary="Prometheus metrics")
def prometheus_metrics() -> Response:
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
