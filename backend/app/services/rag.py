import re
import time
from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Session

from ..core.metrics import rag_latency, rag_requests
from ..services.embeddings import hash_embedding
from ..schemas.rag import RAGChunk


def _redact_pii(text: str) -> str:
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[email]", text)
    text = re.sub(r"\b\+?\d{1,3}?\s?-?\(?\d{2,4}\)?\s?-?\d{2,4}\s?-?\d{2,4}\b", "[phone]", text)
    return text


def search_chunks(query: str, k: int, db: Session) -> List[RAGChunk]:
    rag_requests.inc()
    start = time.perf_counter()
    embedding = hash_embedding(query)
    emb_str = "[" + ",".join(str(v) for v in embedding) + "]"
    stmt = text(
        """
        SELECT source, position, text
        FROM chunks
        ORDER BY embedding <-> (:emb)::vector
        LIMIT :k
        """
    )
    rows = db.execute(stmt, {"emb": emb_str, "k": k}).fetchall()
    rag_latency.observe(time.perf_counter() - start)
    return [RAGChunk(source=r.source, position=r.position, text=_redact_pii(r.text)) for r in rows]
