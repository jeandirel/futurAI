import structlog
from redis import Redis

from ..core.settings import settings

logger = structlog.get_logger(__name__)


def _client() -> Redis:
    return Redis.from_url(settings.redis_url, decode_responses=True)


def enqueue_job(job_id: str) -> None:
    r = _client()
    r.lpush("jobs", job_id)
    logger.info("job_enqueued", job_id=job_id)


def dequeue_job(block: bool = True, timeout: int = 5) -> str | None:
    r = _client()
    if block:
        item = r.brpop("jobs", timeout=timeout)
        return item[1] if item else None
    item = r.rpop("jobs")
    return item
