import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from backend.app.services.embeddings import hash_embedding

CHUNKS_PATH = Path("data/processed/chunks/chunks.jsonl")
SQL_OUT = Path("data/processed/chunks/chunks.sql")


def main() -> None:
    if not CHUNKS_PATH.exists():
        raise SystemExit(f"Missing chunks file at {CHUNKS_PATH}")
    lines = []
    with CHUNKS_PATH.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            emb = hash_embedding(item["text"])
            emb_str = ",".join(f"{v:.6f}" for v in emb)
            text_sql = item["text"].replace("'", "''")
            source_sql = item.get("source", "").replace("'", "''")
            position = int(item.get("position", 0))
            lines.append(
                f"INSERT INTO chunks (id, source, position, text, embedding) "
                f"VALUES (gen_random_uuid(), '{source_sql}', {position}, '{text_sql}', "
                f"vector[{emb_str}]);"
            )
    SQL_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote SQL with {len(lines)} inserts to {SQL_OUT}")


if __name__ == "__main__":
    main()
