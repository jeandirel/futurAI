from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from pgvector.sqlalchemy import Vector

from ..schemas.base import Bloom, Difficulty, Language, Solo

Base = declarative_base()


def default_uuid():
    return str(uuid4())


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=False), primary_key=True, default=default_uuid)
    status = Column(String(32), nullable=False, server_default="pending")
    subject = Column(String(255), nullable=False)
    level = Column(String(255), nullable=False)
    language = Column(String(8), nullable=False)
    count = Column(Integer, nullable=False, server_default=text("1"))
    message = Column(String(1024))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("AgentMessage", back_populates="job")
    mcq_items = relationship("MCQ", back_populates="job")
    fairness_metrics = relationship("FairnessMetric", back_populates="job")


class AgentMessage(Base):
    __tablename__ = "agent_messages"

    id = Column(UUID(as_uuid=False), primary_key=True, default=default_uuid)
    job_id = Column(UUID(as_uuid=False), ForeignKey("jobs.id"), nullable=False)
    agent = Column(String(64), nullable=False)
    role = Column(String(32), nullable=False)
    content = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    job = relationship("Job", back_populates="messages")


class MCQ(Base):
    __tablename__ = "mcq"

    id = Column(UUID(as_uuid=False), primary_key=True, default=default_uuid)
    job_id = Column(UUID(as_uuid=False), ForeignKey("jobs.id"), nullable=False)
    question = Column(String, nullable=False)
    options = Column(JSON, nullable=False)
    answer = Column(String, nullable=False)
    bloom = Column(Enum(Bloom, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    solo = Column(Enum(Solo, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    difficulty = Column(Enum(Difficulty, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    language = Column(Enum(Language, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    topic = Column(String(255), nullable=False)
    source = Column(String(255))
    notes = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    job = relationship("Job", back_populates="mcq_items")


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=False), primary_key=True, default=default_uuid)
    name = Column(String(255), nullable=False)
    path = Column(String(1024), nullable=False)
    meta = Column("meta", JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class FairnessMetric(Base):
    __tablename__ = "fairness_metrics"

    id = Column(UUID(as_uuid=False), primary_key=True, default=default_uuid)
    job_id = Column(UUID(as_uuid=False), ForeignKey("jobs.id"), nullable=False)
    metric = Column(String(255), nullable=False)
    group_key = Column(String(255), nullable=True)
    group_value = Column(String(255), nullable=True)
    value = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    job = relationship("Job", back_populates="fairness_metrics")


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(UUID(as_uuid=False), primary_key=True, default=default_uuid)
    source = Column(String(255), nullable=False)
    position = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    embedding = Column(Vector(128), nullable=False)
    doc_id = Column(UUID(as_uuid=False), ForeignKey("documents.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
