from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.session import get_session
from ..schemas.base import MCQItem
from ..schemas.rag import RAGQuery, RAGResponse
from ..services.generator import generate_mcq_from_rag
from ..services.healing import heal_generation
from ..services.rag import search_chunks

router = APIRouter()


@router.post("/search", response_model=RAGResponse, summary="Recherche RAG (top k chunks)")
def rag_search(payload: RAGQuery, db: Session = Depends(get_session)) -> RAGResponse:
    try:
        chunks = search_chunks(payload.query, payload.k, db)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return RAGResponse(chunks=chunks)


@router.post("/generate", response_model=MCQItem, summary="Generation MCQ simple a partir du RAG")
def rag_generate(payload: RAGQuery, db: Session = Depends(get_session)) -> MCQItem:
    try:
        mcq = generate_mcq_from_rag(payload.query, db, k=payload.k)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return mcq


@router.post("/generate/heal", response_model=MCQItem, summary="Generation MCQ avec healing simple")
def rag_generate_heal(payload: RAGQuery) -> MCQItem:
    return heal_generation(payload, max_attempts=3)
