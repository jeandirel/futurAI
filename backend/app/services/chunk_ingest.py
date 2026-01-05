import json
from pathlib import Path

from sqlalchemy import select

from ..db.base import Chunk, Document
from ..db.session import SessionLocal
from ..services.embeddings import hash_embedding


def ingest_chunks(jsonl_path: Path) -> int:
    session = SessionLocal()
    count = 0
    doc_cache = {}  # Cache source -> doc_id to avoid repeated DB hits
    chunk_buffer = []
    BATCH_SIZE = 1000

    try:
        with jsonl_path.open(encoding="utf-8-sig") as f:
            for line in f:
                if not line.strip():
                    continue
                item = json.loads(line)
                source = item.get("source", "unknown")
                
                # Resolve Document ID (Cached or DB)
                if source not in doc_cache:
                    doc = session.execute(select(Document).where(Document.name == source)).scalar_one_or_none()
                    if not doc:
                        doc = Document(name=source, path=str(source))
                        session.add(doc)
                        session.flush() # Get ID immediately
                    doc_cache[source] = doc.id
                
                doc_id = doc_cache[source]
                
                # Create Chunk object
                text_content = item["text"].replace("\x00", "")
                emb = hash_embedding(text_content)
                chunk = Chunk(
                    source=source,
                    position=item.get("position", 0),
                    text=text_content,
                    embedding=emb,
                    doc_id=doc_id,
                )
                chunk_buffer.append(chunk)
                count += 1
                
                # Bulk Insert
                if len(chunk_buffer) >= BATCH_SIZE:
                    session.bulk_save_objects(chunk_buffer)
                    session.commit()
                    chunk_buffer.clear()
                    print(f"Ingested {count} chunks...")
        
        # Flush remaining
        if chunk_buffer:
            session.bulk_save_objects(chunk_buffer)
            session.commit()
            
    finally:
        session.close()
    return count


if __name__ == "__main__":
    path = Path("data/processed/chunks/chunks.jsonl")
    if not path.exists():
        raise SystemExit(f"Missing chunks file at {path}")
    total = ingest_chunks(path)
    print(f"Ingested {total} chunks into Postgres")
