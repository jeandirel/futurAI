from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from .base import Language, MCQItem


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


class GenerateRequest(BaseModel):
    subject: str = Field(..., description="Subject or topic requested by user")
    level: str = Field(..., description="Level or course name")
    language: Language = Language.fr
    count: int = Field(1, ge=1, le=10, description="Number of MCQ to generate")
    context: Optional[str] = Field(None, description="Optional extra context or instructions")


class JobInfo(BaseModel):
    job_id: str
    status: JobStatus
    message: Optional[str] = None


class GenerateResponse(BaseModel):
    job: JobInfo
    items: Optional[list[MCQItem]] = None


class JobSummary(BaseModel):
    job_id: str
    status: JobStatus
    subject: str
    level: str
    language: Language
    count: int
    message: Optional[str] = None
    created_at: Optional[str] = None


class JobDetail(JobSummary):
    items: Optional[List[MCQItem]] = None
