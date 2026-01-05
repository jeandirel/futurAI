import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parents[1]))

from backend.app.agents.feedback import FeedbackAgent
from backend.app.agents.fairness import FairnessAgent
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language

def test_manual():
    print("=== Test Manuel : Feedback & Fairness ===\n")
    
    # Create sample items
    items = [
        MCQItem(
            question="Quelle est la capitale de la France ?",
            options=["Paris", "Lyon"],
            answer="Paris",
            bloom=Bloom.remember,
            solo=Solo.unistructural,
            difficulty=Difficulty.easy,
            language=Language.fr,
            topic="Geo",
            source="Test"
        ),
        MCQItem(
            question="You are stupid", # Toxic
            options=["Yes", "No"],
            answer="Yes",
            bloom=Bloom.remember,
            solo=Solo.unistructural,
            difficulty=Difficulty.easy,
            language=Language.en,
            topic="Toxic",
            source="Test"
        )
    ]

    # 1. Test Feedback Agent
    print("1. Test Feedback Agent (Explications)...")
    fb_agent = FeedbackAgent()
    results = fb_agent.run(items)
    for res in results:
        print(f"Question: {res['question']}")
        print(f"Explication: {res['explanation']}")
        print("-" * 20)
    print("\n")

    # 2. Test Fairness Agent
    print("2. Test Fairness Agent (Métriques)...")
    fair_agent = FairnessAgent()
    metrics = fair_agent.run(items, group_field="language")
    
    print(f"Total Items: {metrics['total']}")
    print(f"Acceptance Rate: {metrics['acceptance_rate']}")
    print("Group Stats:")
    for grp, stats in metrics["fairness"]["groups"].items():
        print(f"  [{grp}] Count: {stats['count']}, Toxicity Rate: {stats['toxicity_rate']}")

if __name__ == "__main__":
    test_manual()
