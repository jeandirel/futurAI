import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parents[1]))

from backend.app.core.settings import settings
from backend.app.services.llm import generate_text_hf

def test_llm():
    print(f"Testing LLM: {settings.hf_model_id}")
    print(f"Using Token: {settings.hf_api_token[:4]}...{settings.hf_api_token[-4:]}")
    
    try:
        response = generate_text_hf("Say 'Hello World' in French.")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_llm()
