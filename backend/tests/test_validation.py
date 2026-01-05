import pytest

from backend.app.schemas.base import Bloom, Difficulty, Language, MCQItem, Solo
from backend.app.services.validation import validate_mcq


def make_mcq(**kwargs):
    base = dict(
        question="Q?",
        options=["A", "B"],
        answer="A",
        bloom=Bloom.remember,
        solo=Solo.unistructural,
        difficulty=Difficulty.easy,
        language=Language.fr,
        topic="t",
    )
    base.update(kwargs)
    return MCQItem(**base)


def test_validate_ok():
    validate_mcq(make_mcq())


@pytest.mark.parametrize(
    "question",
    ["", " "],
)
def test_validate_question_empty(question):
    with pytest.raises(ValueError):
        validate_mcq(make_mcq(question=question))


def test_validate_options_unique():
    with pytest.raises(ValueError):
        validate_mcq(make_mcq(options=["A", "A"], answer="A"))


def test_validate_answer_missing():
    with pytest.raises(ValueError):
        validate_mcq(make_mcq(options=["A", "B"], answer="C"))


def test_validate_too_many_options():
    with pytest.raises(ValueError):
        validate_mcq(make_mcq(options=["A", "B", "C", "D", "E", "F", "G"], answer="A"))
