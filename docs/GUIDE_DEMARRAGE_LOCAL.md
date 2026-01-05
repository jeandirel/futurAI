# Guide d'Exécution Locale (Sans Docker)

Ce guide explique comment lancer le projet manuellement sur votre machine.

## Prérequis

1.  **Python 3.10+** installé.
2.  **PostgreSQL** installé et en cours d'exécution.
    *   Assurez-vous d'avoir l'extension `pgvector` installée (ou utilisez une image docker juste pour la DB : `docker run -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=oneclickquiz ankane/pgvector`).
3.  **Redis** installé et en cours d'exécution (port 6379).

## Installation

1.  **Backend**
    ```powershell
    cd backend
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

2.  **Frontend**
    ```powershell
    cd frontend
    pip install -r requirements.txt
    ```

## Configuration

1.  Copiez `config/.env.example` vers `config/.env`.
2.  Modifiez `config/.env` si vos identifiants Postgres/Redis diffèrent des valeurs par défaut (`localhost`).

## Lancement

Il faut lancer 3 terminaux séparés :

**Terminal 1 : API Backend**
```powershell
# Depuis la racine du projet
.venv\Scripts\Activate.ps1

# Initialiser la DB (si première fois)
cd backend
alembic upgrade head 
cd ..

# Lancer le serveur
uvicorn backend.app.main:app --reload --port 8000
```

**Terminal 2 : Worker (Traitement des jobs)**
```powershell
# Depuis la racine du projet
.venv\Scripts\Activate.ps1
python -m backend.app.worker
```

**Terminal 3 : Frontend (Streamlit)**
```powershell
cd frontend
# Assurez-vous d'avoir les libs installées (ou utilisez le même venv que backend si compatible, sinon créez-en un autre)
streamlit run app.py
```

Accédez ensuite à :
- Frontend : http://localhost:8501
- API Docs : http://localhost:8000/docs
