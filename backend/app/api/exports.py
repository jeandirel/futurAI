import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from ..db.base import Job
from ..db.session import get_session

router = APIRouter()


@router.get("/jobs/{job_id}/export", summary="Export MCQ of a job as CSV or JSON")
def export_job(job_id: str, format: str = Query(default="json"), db: Session = Depends(get_session)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    items = job.mcq_items
    if format == "json":
        data = [
            {
                "question": m.question,
                "options": m.options,
                "answer": m.answer,
                "bloom": m.bloom,
                "solo": m.solo,
                "difficulty": m.difficulty,
                "language": m.language,
                "topic": m.topic,
                "source": m.source,
                "notes": m.notes,
            }
            for m in items
        ]
        return data
    elif format == "csv":
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["question", "options", "answer", "bloom", "solo", "difficulty", "language", "topic", "source", "notes"])
        for m in items:
            writer.writerow(
                [
                    m.question,
                    "|".join(m.options),
                    m.answer,
                    m.bloom,
                    m.solo,
                    m.difficulty,
                    m.language,
                    m.topic,
                    m.source or "",
                    m.notes or "",
                ]
            )
        return Response(content=buf.getvalue(), media_type="text/csv")
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")
