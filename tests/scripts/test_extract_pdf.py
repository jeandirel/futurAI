import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parents[2]))

from scripts.extract_pdf_text import extract_single_pdf

def test_extract_single_pdf_success(tmp_path):
    # Mock PyPDF2
    with patch("scripts.extract_pdf_text.PyPDF2.PdfReader") as mock_reader:
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Page text"
        mock_reader.return_value.pages = [mock_page]
        
        # Mock OUT_DIR
        with patch("scripts.extract_pdf_text.OUT_DIR", tmp_path):
            pdf_path = Path("test.pdf")
            result = extract_single_pdf(pdf_path)
            
            assert "[OK]" in result
            assert (tmp_path / "test.txt").exists()
            assert (tmp_path / "test.txt").read_text(encoding="utf-8") == "Page text"

def test_extract_single_pdf_error(tmp_path):
    with patch("scripts.extract_pdf_text.PyPDF2.PdfReader") as mock_reader:
        mock_reader.side_effect = Exception("Corrupt PDF")
        
        with patch("scripts.extract_pdf_text.OUT_DIR", tmp_path):
            pdf_path = Path("bad.pdf")
            result = extract_single_pdf(pdf_path)
            
            assert "[ERR]" in result
            assert "Corrupt PDF" in result
