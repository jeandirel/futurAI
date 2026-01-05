import pytest
from unittest.mock import patch
from backend.app.services.validation import validate_mcq
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language

@pytest.fixture
def valid_mcq():
    return MCQItem(
        question="Quelle est la capitale de la France ?",
        options=["Paris", "Lyon", "Marseille"],
        answer="Paris",
        bloom=Bloom.remember,
        solo=Solo.unistructural,
        difficulty=Difficulty.easy,
        language=Language.fr,
        topic="Geo",
        source="Test"
    )

def test_validate_mcq_valid(valid_mcq):
    validate_mcq(valid_mcq) # Should not raise

def test_validate_mcq_empty_question(valid_mcq):
    valid_mcq.question = ""
    with pytest.raises(ValueError, match="Question vide"):
        validate_mcq(valid_mcq)

def test_validate_mcq_too_few_options(valid_mcq):
    valid_mcq.options = ["Paris"]
    with pytest.raises(ValueError, match="Moins de 2 options"):
        validate_mcq(valid_mcq)

def test_validate_mcq_duplicate_options(valid_mcq):
    valid_mcq.options = ["Paris", "Paris"]
    with pytest.raises(ValueError, match="Options dupliquees"):
        validate_mcq(valid_mcq)

def test_validate_mcq_answer_not_in_options(valid_mcq):
    valid_mcq.answer = "Bordeaux"
    with pytest.raises(ValueError, match="Reponse absente"):
        validate_mcq(valid_mcq)

def test_validate_mcq_pii_email(valid_mcq):
    valid_mcq.question = "Contactez moi a test@example.com"
    with pytest.raises(ValueError, match="PII detectee"):
        validate_mcq(valid_mcq)

def test_validate_mcq_toxicity(valid_mcq):
    with patch("backend.app.services.validation.settings.use_toxicity", True):
        with patch("backend.app.services.validation.is_toxic", return_value=True):
            with pytest.raises(ValueError, match="Toxicite detectee"):
                validate_mcq(valid_mcq)
