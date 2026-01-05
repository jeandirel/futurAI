"""
Chunk plaintext files from data/processed into JSONL ready for embeddings.
Each chunk stores text, source_name, language (optional), and position.
"""

import json
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
OUT_DIR = Path("data/processed/chunks")

# Simple chunking by characters; adjust if needed (e.g., by tokens)
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200


def chunk_text(text: str, size: int, overlap: int):
    n = len(text)
    step = max(1, size - overlap)
    for start in range(0, n, step):
        end = min(n, start + size)
        yield text[start:end]


def process_file(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    chunks = []
    for idx, chunk in enumerate(chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)):
        if not chunk.strip():
            continue
        chunks.append(
            {
                "source": path.name,
                "position": idx,
                "text": chunk.strip(),
            }
        )
    return chunks


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "chunks.jsonl"
    total = 0
    with out_path.open("w", encoding="utf-8") as f:
        for file in PROCESSED_DIR.glob("*.txt"):
            items = process_file(file)
            for item in items:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
            total += len(items)
    print(f"Wrote chunks to {out_path} with {total} chunks")


if __name__ == "__main__":
    main()
