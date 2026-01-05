import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parents[1]))

from backend.app.agents.validation import ValidationAgent
from backend.app.schemas.base import MCQItem, Bloom, Solo, Difficulty, Language

def test_manual():
    print("=== Test Manuel : Agent de Validation ===\n")
    agent = ValidationAgent()

    # 1. Test Valid MCQ
    print("1. Test QCM Valide...")
    valid_mcq = MCQItem(
        question="Quelle est la capitale de la France ?",
        options=["Paris", "Lyon", "Marseille"],
        answer="Paris",
        bloom=Bloom.remember,
        solo=Solo.unistructural,
        difficulty=Difficulty.easy,
        language=Language.fr,
        topic="Géographie",
        source="Manuel"
    )
    try:
        agent.run([valid_mcq])
        print("✅ SUCCÈS : QCM valide accepté.\n")
    except Exception as e:
        print(f"❌ ÉCHEC : {e}\n")

    # 2. Test PII (Email)
    print("2. Test Détection PII (Email)...")
    pii_mcq = MCQItem(
        question="Envoyez vos réponses à admin@example.com",
        options=["D'accord", "Pas d'accord"],
        answer="D'accord",
        bloom=Bloom.remember,
        solo=Solo.unistructural,
        difficulty=Difficulty.easy,
        language=Language.fr,
        topic="Privacy",
        source="Manuel"
    )
    try:
        agent.run([pii_mcq])
        print("❌ ÉCHEC : QCM avec PII aurait dû être rejeté.\n")
    except ValueError as e:
        print(f"✅ SUCCÈS : Rejeté correctement ({e})\n")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}\n")

    # 3. Test Structure (Options manquantes)
    print("3. Test Structure (1 seule option)...")
    bad_struct_mcq = MCQItem(
        question="Question ?",
        options=["Unique Option"],
        answer="Unique Option",
        bloom=Bloom.remember,
        solo=Solo.unistructural,
        difficulty=Difficulty.easy,
        language=Language.fr,
        topic="Structure",
        source="Manuel"
    )
    try:
        agent.run([bad_struct_mcq])
        print("❌ ÉCHEC : QCM mal formé aurait dû être rejeté.\n")
    except ValueError as e:
        print(f"✅ SUCCÈS : Rejeté correctement ({e})\n")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}\n")

if __name__ == "__main__":
    test_manual()
