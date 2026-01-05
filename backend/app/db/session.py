from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..core.settings import settings

engine = create_engine(
    settings.postgres_dsn,
    echo=False,
    future=True,
    pool_size=20,           # Increase pool size for concurrency
    max_overflow=10,        # Allow temporary extra connections
    pool_pre_ping=True,     # Check connection health before usage
    pool_recycle=3600,      # Recycle connections every hour
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
