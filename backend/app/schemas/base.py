from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Language(str, Enum):
    fr = "fr"
    en = "en"


class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Bloom(str, Enum):
    remember = "remember"
    understand = "understand"
    apply = "apply"
    analyze = "analyze"
    evaluate = "evaluate"
    create = "create"


class Solo(str, Enum):
    prestructural = "prestructural"
    unistructural = "unistructural"
    multistructural = "multistructural"
    relational = "relational"
    extended = "extended"


class MCQItem(BaseModel):
    question: str
    options: List[str] = Field(min_length=2, max_length=6)
    answer: str
    bloom: Bloom
    solo: Solo
    difficulty: Difficulty
    language: Language
    topic: str
    source: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        str_strip_whitespace = True
        use_enum_values = True
