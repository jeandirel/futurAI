import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parents[1]))

from backend.app.core.settings import settings
from backend.app.services.llm import generate_mcq_gemini

def test_gemini():
    print(f"Testing Gemini: {settings.google_model_id}")
    print(f"Using Key: {settings.google_api_key[:4]}...{settings.google_api_key[-4:]}")
    
    try:
        mcq = generate_mcq_gemini("Qu'est-ce que le RAG ?", ["Le RAG (Retrieval Augmented Generation) combine recherche documentaire et generation de texte."])
        print(f"Success! Generated MCQ:\n{mcq.model_dump_json(indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_gemini()
