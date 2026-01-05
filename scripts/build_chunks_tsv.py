import csv
import sys
from pathlib import Path
from uuid import uuid4

import hashlib
import struct
import json

ROOT = Path(__file__).resolve().parents[1]
CHUNKS_PATH = ROOT / "data/processed/chunks/chunks.jsonl"
TSV_OUT = ROOT / "data/processed/chunks/chunks.tsv"


def hash_embedding(text: str, dim: int = 128):
    h = hashlib.sha256(text.encode("utf-8", errors="ignore")).digest()
    vals = []
    while len(vals) < dim:
        h = hashlib.sha256(h).digest()
        for i in range(0, len(h), 4):
            if len(vals) >= dim:
                break
            chunk = h[i : i + 4]
            val = struct.unpack(">I", chunk)[0] / 0xFFFFFFFF
            vals.append(val)
    return vals


def main() -> None:
    if not CHUNKS_PATH.exists():
        raise SystemExit(f"Missing chunks JSONL at {CHUNKS_PATH}")
    with CHUNKS_PATH.open(encoding="utf-8") as fin, TSV_OUT.open("w", encoding="utf-8", newline="") as fout:
        writer = csv.writer(fout, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        count = 0
        for line in fin:
            if not line.strip():
                continue
            item = json.loads(line)
            emb = hash_embedding(item["text"])
            emb_str = "[" + ",".join(f"{v:.6f}" for v in emb) + "]"
            writer.writerow(
                [
                    str(uuid4()),
                    item.get("source", ""),
                    int(item.get("position", 0)),
                    item["text"],
                    emb_str,
                ]
            )
            count += 1
    print(f"Wrote TSV with {count} rows to {TSV_OUT}")


if __name__ == "__main__":
    main()
