"""
Archivist/KG agent: ingestion et gestion d'index (placeholder).
"""

from pathlib import Path
from typing import List


class ArchivistAgent:
    def ingest(self, paths: List[Path]) -> dict:
        """
        Ingest files. Currently supports .jsonl files via ingest_chunks.
        For other files, returns 'not_implemented'.
        """
        from backend.app.services.chunk_ingest import ingest_chunks
        
        results = {}
        for p in paths:
            if p.suffix == ".jsonl":
                try:
                    count = ingest_chunks(p)
                    results[str(p)] = f"ingested_{count}_chunks"
                except Exception as e:
                    results[str(p)] = f"error: {str(e)}"
            else:
                results[str(p)] = "skipped_not_jsonl"
                
        return {"results": results}
