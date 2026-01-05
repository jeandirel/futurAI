"""
LLM clients :
- Placeholder local
- Hugging Face Inference API (texte -> MCQ)
"""

import os
import re
from typing import List, Optional

import requests
import structlog

from ..core.settings import settings
from ..schemas.base import Bloom, Difficulty, Language, MCQItem, Solo

logger = structlog.get_logger(__name__)


def generate_mcq_placeholder(query: str, contexts: List[str]) -> MCQItem:
    context_preview = contexts[0][:120] if contexts else query
    question = f"Selon le contexte suivant, repondez : {context_preview}"
    options = ["Option A", "Option B", "Option C", "Option D"]
    answer = options[0]
    return MCQItem(
        question=question,
        options=options,
        answer=answer,
        bloom=Bloom.understand,
        solo=Solo.unistructural,
        difficulty=Difficulty.easy,
        language=Language.fr,
        topic="RAG",
        source="LLM",
        notes="Genere via LLM placeholder",
    )


def _hf_headers() -> dict:
    token = settings.hf_api_token or os.environ.get("HF_API_TOKEN")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _prompt_mcq(query: str, contexts: List[str], level: str = None, language: str = "fr", previous_questions: List[str] = None) -> str:
    ctx = "\n".join(contexts[:3])
    lang_instruction = "en français" if language == "fr" else "in English"
    level_instruction = f"Niveau cible : {level}." if level else ""
    
    avoid_instruction = ""
    if previous_questions:
        avoid_list = "\n- ".join(previous_questions[-5:]) # Keep only last 5 to avoid huge prompt
        avoid_instruction = f"5. DIVERSITÉ : Ne pose PAS les mêmes questions que celles-ci :\n- {avoid_list}\n"

    return (
        f"Tu es un expert pédagogique. Ton but est de créer une question à choix multiples (QCM) pertinente basée sur le texte fourni.\n"
        f"RÈGLES STRICTES :\n"
        f"1. Réponds UNIQUEMENT au format JSON valide. Pas de texte avant ou après.\n"
        f"2. Le JSON doit contenir les clés : question, options (liste de 4 chaines), answer (doit être une des options), bloom, solo, difficulty.\n"
        f"3. La question doit être {lang_instruction}, claire et sans ambiguïté.\n"
        f"4. Les options doivent être plausibles.\n"
        f"{avoid_instruction}"
        f"{level_instruction}\n"
        f"Contexte:\n{ctx}\n"
        f"Sujet à couvrir: {query}\n"
    )


def _parse_hf_json(text: str) -> dict | None:
    try:
        import json
        # Nettoyage des blocs markdown common avec Llama 3
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        data = json.loads(text.strip())
        if isinstance(data, list):
            # If LLM returns a list of items, take the first one
            data = data[0] if data else {}
        return _normalize_enums(data)
    except Exception:
        return None

def _normalize_enums(data: dict) -> dict:
    # Map French/Capitalized values to English Enums
    bloom_map = {
        "connaissance": "remember", "mémorisation": "remember", "remember": "remember",
        "compréhension": "understand", "understand": "understand",
        "application": "apply", "apply": "apply",
        "analyse": "analyze", "analyze": "analyze",
        "évaluation": "evaluate", "evaluate": "evaluate",
        "création": "create", "create": "create"
    }
    solo_map = {
        "unistructurel": "unistructural", "unistructural": "unistructural",
        "multistructurel": "multistructural", "multistructural": "multistructural",
        "relationnel": "relational", "relational": "relational",
        "abstrait étendu": "extended", "extended": "extended"
    }
    diff_map = {
        "facile": "easy", "easy": "easy",
        "moyen": "medium", "medium": "medium",
        "difficile": "hard", "hard": "hard",
        "1": "easy", "2": "medium", "3": "hard" # Handle string integers
    }
    
    if "bloom" in data:
        if isinstance(data["bloom"], bool):
            data["bloom"] = "understand"
        elif isinstance(data["bloom"], str):
            data["bloom"] = bloom_map.get(data["bloom"].lower(), "understand")
            
    if "solo" in data:
        if isinstance(data["solo"], bool):
            data["solo"] = "unistructural"
        elif isinstance(data["solo"], str):
            data["solo"] = solo_map.get(data["solo"].lower(), "unistructural")
            
    if "difficulty" in data:
        if isinstance(data["difficulty"], bool):
            data["difficulty"] = "easy"
        elif isinstance(data["difficulty"], int):
            # Handle integer difficulty (1, 2, 3)
            if data["difficulty"] == 1: data["difficulty"] = "easy"
            elif data["difficulty"] == 2: data["difficulty"] = "medium"
            elif data["difficulty"] >= 3: data["difficulty"] = "hard"
            else: data["difficulty"] = "easy"
        elif isinstance(data["difficulty"], str):
            data["difficulty"] = diff_map.get(data["difficulty"].lower(), "easy")
        
    return data


def _fallback_parse(text: str) -> dict:
    # heuristique: chercher lignes commençant par - ou *
    lines = [l.strip(" -*") for l in text.splitlines() if l.strip()]
    question = lines[0] if lines else "Question generee"
    options = [l for l in lines[1:] if l]
    if len(options) < 2:
        options = ["Option A", "Option B"]
    answer = options[0]
    return {
        "question": question,
        "options": options,
        "answer": answer,
        "bloom": "understand",
        "solo": "unistructural",
        "difficulty": "easy",
    }


def generate_mcq_hf(query: str, contexts: List[str], level: str = None, language: str = "fr", previous_questions: List[str] = None) -> MCQItem:
    if not settings.hf_model_id:
        raise ValueError("HF_MODEL_ID manquant")
    payload = {"inputs": _prompt_mcq(query, contexts, level, language, previous_questions)}
    base = settings.hf_api_base.rstrip("/")

    def _call(model_id: str) -> requests.Response:
        return requests.post(
            f"{base}/models/{model_id}",
            headers=_hf_headers(),
            json=payload,
            timeout=settings.hf_timeout,
        )

    resp: Optional[requests.Response] = None
    try:
        resp = _call(settings.hf_model_id)
        resp.raise_for_status()
    except requests.HTTPError as exc:
        # Si le modèle n'est pas servable (404), tenter un fallback public
        if getattr(exc.response, "status_code", None) == 404 and settings.hf_fallback_model:
            resp = _call(settings.hf_fallback_model)
            resp.raise_for_status()
        else:
            raise

    content = resp.json()
    # content peut être str ou liste; normaliser
    if isinstance(content, list) and content and isinstance(content[0], dict) and "generated_text" in content[0]:
        text = content[0]["generated_text"]
    elif isinstance(content, str):
        text = content
    else:
        text = str(content)
    data = _parse_hf_json(text) or _fallback_parse(text)
    options = data.get("options") or ["Option A", "Option B"]
    answer = data.get("answer") or options[0]
    return MCQItem(
        question=data.get("question") or "Question generee",
        options=options,
        answer=answer,
        bloom=Bloom(data.get("bloom", "understand")),
        solo=Solo(data.get("solo", "unistructural")),
        difficulty=Difficulty(data.get("difficulty", "easy")),
        language=Language.fr,
        topic="RAG",
        source="HF",
        notes="Genere via HuggingFace Inference API",
    )


def generate_text_hf(prompt: str) -> str:
    if not settings.hf_model_id:
        raise ValueError("HF_MODEL_ID manquant")
    base = settings.hf_api_base.rstrip("/")
    resp = requests.post(
        f"{base}/models/{settings.hf_model_id}",
        headers=_hf_headers(),
        json={"inputs": prompt},
        timeout=settings.hf_timeout,
    )
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, list) and data and isinstance(data[0], dict) and "generated_text" in data[0]:
        return str(data[0]["generated_text"])
    if isinstance(data, str):
        return data
    return str(data)


def generate_mcq_gemini(query: str, contexts: List[str], level: str = None, language: str = "fr", previous_questions: List[str] = None) -> MCQItem:
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY manquant")
    
    prompt = _prompt_mcq(query, contexts, level, language, previous_questions)
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.google_model_id}:generateContent?key={settings.google_api_key}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }
    
    resp = requests.post(url, json=payload, timeout=settings.hf_timeout)
    resp.raise_for_status()
    data = resp.json()
    
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise ValueError("Format de reponse Gemini inattendu")

    data_json = _parse_hf_json(text) or _fallback_parse(text)
    
    options = data_json.get("options") or ["Option A", "Option B"]
    answer = data_json.get("answer") or options[0]
    
    return MCQItem(
        question=data_json.get("question") or "Question generee",
        options=options,
        answer=answer,
        bloom=Bloom(data_json.get("bloom", "understand")),
        solo=Solo(data_json.get("solo", "unistructural")),
        difficulty=Difficulty(data_json.get("difficulty", "easy")),
        language=Language.fr,
        topic="RAG",
        source="Gemini",
        notes=f"Genere via Google {settings.google_model_id}",
    )


def generate_mcq_openrouter(query: str, contexts: List[str], level: str = None, language: str = "fr", previous_questions: List[str] = None) -> MCQItem:
    if not settings.openrouter_api_key:
        raise ValueError("OPENROUTER_API_KEY manquant")

    prompt = _prompt_mcq(query, contexts, level, language, previous_questions)
    
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000", # Optional, for OpenRouter rankings
        "X-Title": settings.app_name,
    }
    
    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {"role": "system", "content": "Tu es un expert pedagogique. Reponds uniquement en JSON."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"} # Supported by some models on OpenRouter
    }
    
    resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=settings.hf_timeout)
    resp.raise_for_status()
    data = resp.json()
    
    try:
        text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise ValueError("Format de reponse OpenRouter inattendu")

    data_json = _parse_hf_json(text) or _fallback_parse(text)
    if not data_json:
        # Fallback if parsing fails completely
        pass
    
    options = data_json.get("options") or ["Option A", "Option B"]
    answer = data_json.get("answer") or options[0]
    
    return MCQItem(
        question=data_json.get("question") or "Question generee",
        options=options,
        answer=answer,
        bloom=Bloom(data_json.get("bloom", "understand")),
        solo=Solo(data_json.get("solo", "unistructural")),
        difficulty=Difficulty(data_json.get("difficulty", "easy")),
        language=Language.fr,
        topic="RAG",
        source="OpenRouter",
        notes=f"Genere via {settings.openrouter_model}",
    )


def generate_text_openrouter(prompt: str) -> str:
    if not settings.openrouter_api_key:
        raise ValueError("OPENROUTER_API_KEY manquant")
    
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": settings.app_name,
    }
    
    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=settings.hf_timeout)
    resp.raise_for_status()
    data = resp.json()
    
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return "Erreur format OpenRouter"


def generate_text(prompt: str) -> str:
    """Generic text generation dispatching to configured provider."""
    if settings.llm_provider == "openrouter":
        return generate_text_openrouter(prompt)
    elif settings.llm_provider == "gemini":
        # Placeholder for Gemini text gen if needed later
        return "Gemini text gen not implemented yet"
    else:
        return generate_text_hf(prompt)
