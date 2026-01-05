import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(str(Path(__file__).parents[1]))

from backend.app.services.healing import heal_generation
from backend.app.schemas.rag import RAGQuery
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language

def test_manual():
    print("=== Test Manuel : Agent Healing (Auto-réparation) ===\n")
    
    # Valid MCQ to return on success
    valid_mcq = MCQItem(
        question="Quelle est la capitale de la France ?",
        options=["Paris", "Lyon", "Marseille"],
        answer="Paris",
        bloom=Bloom.remember,
        solo=Solo.unistructural,
        difficulty=Difficulty.easy,
        language=Language.fr,
        topic="Geo",
        source="Healing"
    )

    print("Scénario : La génération échoue 2 fois, puis réussit.")
    print("On s'attend à voir des logs de 'retry'...\n")

    # Mocking generate_mcq_from_rag to fail twice then succeed
    with patch("backend.app.services.healing.generate_mcq_from_rag") as mock_gen:
        with patch("backend.app.services.healing.SessionLocal"): # Mock DB
             # Side effect: Exception, Exception, Success
            mock_gen.side_effect = [
                ValueError("Erreur simulée: Question vide"),
                ValueError("Erreur simulée: Pas assez d'options"),
                valid_mcq
            ]
            
            try:
                payload = RAGQuery(query="Test Healing", k=1)
                result = heal_generation(payload, max_attempts=3)
                
                print("\n✅ SUCCÈS FINAL : QCM généré après réparation.")
                print(f"Question: {result.question}")
                print(f"Source: {result.source}")
                print(f"Tentatives nécessaires: {mock_gen.call_count}")
                
            except Exception as e:
                print(f"❌ ÉCHEC : {e}")

if __name__ == "__main__":
    test_manual()
