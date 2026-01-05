import re

from backend.app.schemas.base import MCQItem
from backend.app.core.settings import settings
from backend.app.services.toxicity import is_toxic


def _contains_pii(text: str) -> bool:
    # simple checks emails/phones
    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phone = re.search(r"\b\+?\d{1,3}?\s?-?\(?\d{2,4}\)?\s?-?\d{2,4}\s?-?\d{2,4}\b", text)
    return bool(email or phone)


def validate_mcq(item: MCQItem) -> None:
    if not item.question.strip():
        raise ValueError("Question vide")
    if len(item.question) > 400:
        raise ValueError("Question trop longue")
    if len(item.options) < 2:
        raise ValueError("Moins de 2 options")
    if len(item.options) > 6:
        raise ValueError("Trop d'options")
    if len(item.options) != len(set(item.options)):
        raise ValueError("Options dupliquees")
    if item.answer not in item.options:
        raise ValueError("Reponse absente des options")
    if item.language not in ("fr", "en"):
        raise ValueError("Langue non supportee")
    for opt in item.options:
        if _contains_pii(opt):
            raise ValueError("PII detectee dans les options")
        if settings.use_toxicity and is_toxic(opt):
            raise ValueError("Toxicite detectee dans les options")
    if _contains_pii(item.question):
        raise ValueError("PII detectee dans la question")
    if settings.use_toxicity and is_toxic(item.question):
        raise ValueError("Toxicite detectee dans la question")
