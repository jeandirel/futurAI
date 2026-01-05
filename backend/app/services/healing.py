import structlog
import time
from fastapi import HTTPException

from backend.app.services.generator import generate_mcq_from_rag
from backend.app.services.validation import validate_mcq
from backend.app.schemas.base import MCQItem
from backend.app.schemas.rag import RAGQuery
from backend.app.db.session import SessionLocal
from backend.app.core.metrics import healing_requests, healing_latency

logger = structlog.get_logger(__name__)


def heal_generation(payload: RAGQuery, max_attempts: int = 3, previous_questions: List[str] = None) -> MCQItem:
    """
    Healing loop: regenerate MCQ up to max_attempts if validation fails.
    Uses the validation error to guide the next generation (simulated).
    """
    last_err = None
    start = time.monotonic()
    healing_requests.inc()
    
    # First attempt
    try:
        with SessionLocal() as db:
            mcq = generate_mcq_from_rag(payload.query, db, k=payload.k, level=payload.level, language=payload.language, previous_questions=previous_questions)
        validate_mcq(mcq)
        elapsed = time.monotonic() - start
        healing_latency.observe(elapsed)
        logger.info("healing_success", attempts=1, latency_ms=int(elapsed * 1000))
        return mcq
    except Exception as exc:
        last_err = exc
        logger.warning("healing_first_attempt_failed", error=str(exc))

    # Retry loop with feedback
    for attempt in range(2, max_attempts + 1):
        try:
            # In a real agentic loop, we would append the error to the prompt.
            # For now, we re-generate, potentially the randomness/temperature 
            # or the fallback logic in generator will produce a different result.
            # We explicitly log that we are retrying due to a specific error.
            logger.info("healing_retry_start", attempt=attempt, previous_error=str(last_err))
            
            with SessionLocal() as db:
                # Ideally: generate_mcq_from_rag(..., feedback=str(last_err))
                mcq = generate_mcq_from_rag(payload.query, db, k=payload.k, level=payload.level, language=payload.language, previous_questions=previous_questions)
            
            validate_mcq(mcq)
            
            elapsed = time.monotonic() - start
            healing_latency.observe(elapsed)
            logger.info("healing_success", attempts=attempt, latency_ms=int(elapsed * 1000))
            return mcq
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            elapsed = time.monotonic() - start
            healing_latency.observe(elapsed)
            logger.warning(
                "healing_retry_failed",
                attempts=attempt,
                error=str(exc),
                latency_ms=int(elapsed * 1000),
            )
            
    raise HTTPException(status_code=500, detail=f"Healing failed after {max_attempts} attempts. Last error: {last_err}")
