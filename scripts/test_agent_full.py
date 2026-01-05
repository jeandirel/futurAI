import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parents[1]))

from backend.app.db.session import SessionLocal
from backend.app.agents.generation import GenerationAgent

def main():
    print("Testing Generation Agent (End-to-End)...")
    
    # DB session is required by constructor but not used in run() currently
    db = SessionLocal() 
    agent = GenerationAgent(db)
    
    subject = "Qu'est-ce que l'intelligence artificielle ?"
    print(f"Generating 1 MCQ on: '{subject}'")
    print("Please wait, querying RAG and OpenRouter...")
    
    try:
        items = agent.run(subject, count=1)
        for item in items:
            print("\n" + "="*40)
            print(f"Question:  {item.question}")
            print("-" * 40)
            for opt in item.options:
                print(f"[ ] {opt}")
            print("-" * 40)
            print(f"Answer:    {item.answer}")
            print(f"Source:    {item.source}")
            print(f"Notes:     {item.notes}")
            print("="*40 + "\n")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
