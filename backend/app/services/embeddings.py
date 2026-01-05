import hashlib
import struct
from typing import List


def hash_embedding(text: str, dim: int = 128) -> List[float]:
    """Deterministic pseudo-embedding based on SHA256 hashes (placeholder)."""
    h = hashlib.sha256(text.encode("utf-8", errors="ignore")).digest()
    vals = []
    while len(vals) < dim:
        h = hashlib.sha256(h).digest()
        # unpack into floats in [0,1)
        for i in range(0, len(h), 4):
            if len(vals) >= dim:
                break
            chunk = h[i : i + 4]
            val = struct.unpack(">I", chunk)[0] / 0xFFFFFFFF
            vals.append(val)
    return vals
