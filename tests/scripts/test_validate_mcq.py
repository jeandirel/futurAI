import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parents[2]))

from scripts.validate_mcq_jsonl import validate_item

def test_validate_item_valid():
    item = {
        "question": "Q?",
        "options": ["A", "B"],
        "answer": "A",
        "bloom": "remember",
        "solo": "unistructural",
        "difficulty": "easy",
        "language": "fr",
        "topic": "t",
        "source": "s"
    }
    # Should not raise
    validate_item(item, 1)

def test_validate_item_missing_field():
    item = {"question": "Q?"}
    with pytest.raises(ValueError, match="missing field"):
        validate_item(item, 1)

def test_validate_item_invalid_enum():
    item = {
        "question": "Q?",
        "options": ["A", "B"],
        "answer": "A",
        "bloom": "INVALID",
        "solo": "unistructural",
        "difficulty": "easy",
        "language": "fr",
        "topic": "t",
        "source": "s"
    }
    with pytest.raises(ValueError, match="invalid bloom"):
        validate_item(item, 1)
