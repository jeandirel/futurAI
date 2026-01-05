import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import json
import sys

# Add project root to path to import script
ROOT = Path(__file__).parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from scripts.eval_batch import main

def test_eval_batch_main(tmp_path, capsys):
    # Create a dummy input file
    input_file = tmp_path / "input.json"
    input_data = [
        {
            "question": "Q1", "options": ["A", "B"], "answer": "A",
            "bloom": "remember", "solo": "unistructural", "difficulty": "easy",
            "language": "fr", "topic": "t", "source": "s"
        }
    ]
    input_file.write_text(json.dumps(input_data), encoding="utf-8")
    
    # Mock sys.argv
    with patch.object(sys, 'argv', ["eval_batch.py", str(input_file)]):
        main()
    
    # Check stdout
    captured = capsys.readouterr()
    output = json.loads(captured.out)
    assert output["total"] == 1
    assert output["acceptance_rate"] == 1.0

def test_eval_batch_output_file(tmp_path):
    input_file = tmp_path / "input.json"
    output_file = tmp_path / "output.json"
    input_data = [
        {
            "question": "Q1", "options": ["A", "B"], "answer": "A",
            "bloom": "remember", "solo": "unistructural", "difficulty": "easy",
            "language": "fr", "topic": "t", "source": "s"
        }
    ]
    input_file.write_text(json.dumps(input_data), encoding="utf-8")
    
    with patch.object(sys, 'argv', ["eval_batch.py", str(input_file), "--output", str(output_file)]):
        main()
    
    assert output_file.exists()
    output = json.loads(output_file.read_text(encoding="utf-8"))
    assert output["total"] == 1
