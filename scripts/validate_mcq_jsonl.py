import json
import sys
from pathlib import Path
from typing import Set

REQUIRED_FIELDS = {
    "question": str,
    "options": list,
    "answer": str,
    "bloom": str,
    "solo": str,
    "difficulty": str,
    "language": str,
    "topic": str,
    "source": str,
}

# Pre-compute sets for O(1) lookups
ENUM_BLOOM: Set[str] = {"apply", "analyze", "evaluate", "create", "remember", "understand"}
ENUM_SOLO: Set[str] = {"prestructural", "unistructural", "multistructural", "relational", "extended"}
ENUM_DIFFICULTY: Set[str] = {"easy", "medium", "hard"}
ENUM_LANGUAGE: Set[str] = {"fr", "en"}

def validate_item(item: dict, idx: int) -> None:
    """
    Validate a single MCQ item. Raises ValueError on failure.
    Optimized to fail fast.
    """
    # Check keys existence and type
    for field, typ in REQUIRED_FIELDS.items():
        val = item.get(field)
        if val is None:
            raise ValueError(f"Line {idx}: missing field '{field}'")
        if not isinstance(val, typ):
            raise ValueError(f"Line {idx}: field '{field}' must be {typ.__name__}")

    # Logic checks
    options = item["options"]
    if len(options) < 2:
        raise ValueError(f"Line {idx}: at least 2 options required")
    
    # Check answer presence (O(N) but N is small, usually 4)
    if item["answer"] not in options:
        raise ValueError(f"Line {idx}: answer must be one of the options")

    # Enum checks (O(1))
    if item["bloom"] not in ENUM_BLOOM:
        raise ValueError(f"Line {idx}: invalid bloom '{item['bloom']}'")
    if item["solo"] not in ENUM_SOLO:
        raise ValueError(f"Line {idx}: invalid solo '{item['solo']}'")
    if item["difficulty"] not in ENUM_DIFFICULTY:
        raise ValueError(f"Line {idx}: invalid difficulty '{item['difficulty']}'")
    if item["language"] not in ENUM_LANGUAGE:
        raise ValueError(f"Line {idx}: invalid language '{item['language']}'")


def main(path_str: str) -> None:
    path = Path(path_str)
    if not path.exists():
        raise SystemExit(f"File not found: {path}")
    
    print(f"Validating {path}...")
    valid_count = 0
    error_count = 0
    
    # Use buffering for reading large files
    with path.open("r", encoding="utf-8", buffering=8192*1024) as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                validate_item(item, idx)
                valid_count += 1
            except ValueError as e:
                print(f"[ERR] {e}")
                error_count += 1
            except json.JSONDecodeError as e:
                print(f"[ERR] Line {idx}: invalid JSON: {e}")
                error_count += 1
                
    print(f"\nResult: {valid_count} valid items, {error_count} errors.")
    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/validate_mcq_jsonl.py <path_to_jsonl>")
    main(sys.argv[1])

