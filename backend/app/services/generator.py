import re
import time
from typing import List

from sqlalchemy.orm import Session

import structlog

from ..core.metrics import llm_latency, llm_requests
from ..core.settings import settings
from ..schemas.base import Bloom, Difficulty, Language, MCQItem, Solo
from .rag import search_chunks
from .validation import validate_mcq
from .llm import generate_mcq_placeholder, generate_mcq_hf, generate_mcq_gemini, generate_mcq_openrouter


logger = structlog.get_logger(__name__)


def _clean_text(text: str, max_len: int = 160) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len]


def generate_mcq_from_rag(query: str, db: Session, k: int = 3, level: str = None, language: str = "fr", previous_questions: List[str] = None) -> MCQItem:
    chunks = search_chunks(query, k, db)
    if not chunks:
        logger.warning("rag_no_chunks", query=query)
        if settings.use_llm:
            contexts = [query]
            start = time.perf_counter()
            try:
                mcq = generate_mcq_hf(query, contexts, level, language, previous_questions)
                llm_requests.labels(status="success", model=settings.hf_model_id or "hf").inc()
                llm_latency.observe(time.perf_counter() - start)
                logger.info("mcq_generated_llm", source="hf_no_context", use_llm=settings.use_llm)
            except Exception as exc:  # noqa: BLE001
                logger.warning("mcq_generate_llm_failed", error=str(exc))
                llm_requests.labels(status="error", model=settings.hf_model_id or "hf").inc()
                mcq = generate_mcq_placeholder(query, contexts)
                llm_requests.labels(status="fallback", model="placeholder").inc()
                llm_latency.observe(time.perf_counter() - start)
                logger.info("mcq_generated_llm", source="placeholder_no_context", use_llm=settings.use_llm)
            validate_mcq(mcq)
            return mcq
        raise ValueError("No chunks found for query")
    first = chunks[0]
    if settings.use_llm:
        contexts = [c.text for c in chunks]
        start = time.perf_counter()
        try:
            if settings.llm_provider == "gemini":
                mcq = generate_mcq_gemini(query, contexts, level, language, previous_questions)
                llm_requests.labels(status="success", model=settings.google_model_id).inc()
                logger.info("mcq_generated_llm", source="gemini", use_llm=True)
            elif settings.llm_provider == "openrouter":
                mcq = generate_mcq_openrouter(query, contexts, level, language, previous_questions)
                llm_requests.labels(status="success", model=settings.openrouter_model).inc()
                logger.info("mcq_generated_llm", source="openrouter", use_llm=True)
            else:
                # Prioritize the real HF model; fall back to placeholder if API fails
                mcq = generate_mcq_hf(query, contexts, level, language, previous_questions)
                llm_requests.labels(status="success", model=settings.hf_model_id or "hf").inc()
                logger.info("mcq_generated_llm", source="hf", use_llm=settings.use_llm)
            
            llm_latency.observe(time.perf_counter() - start)
        except Exception as exc:  # noqa: BLE001
            logger.warning("mcq_generate_llm_failed", error=str(exc))
            llm_requests.labels(status="error", model=settings.llm_provider).inc()
            mcq = generate_mcq_placeholder(query, contexts)
            llm_requests.labels(status="fallback", model="placeholder").inc()
            llm_latency.observe(time.perf_counter() - start)
            logger.info("mcq_generated_llm", source="placeholder", use_llm=settings.use_llm)
    else:
        context = _clean_text(first.text)
        question = f"Quel est le sujet principal du passage suivant ? \"{context}\""
        correct = f"{first.source}"
        distractors: List[str] = []
        distractors.append("Sujet non lie au passage")
        if len(chunks) > 1:
            distractors.append(f"{chunks[1].source}")
        distractors.append("Informations generiques")
        options = [correct] + [opt for opt in distractors if opt not in (correct,)]
        options = options[:4]
        mcq = MCQItem(
            question=question,
            options=options,
            answer=correct,
            bloom=Bloom.understand,
            solo=Solo.unistructural,
            difficulty=Difficulty.easy,
            language=Language.fr,
            topic="RAG",
            source=first.source,
            notes="Genere a partir du top-k RAG (placeholder sans LLM).",
        )
    validate_mcq(mcq)
    return mcq
