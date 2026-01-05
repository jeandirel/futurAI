from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_app_title():
    assert app.title == "OneClickQuiz Agents"

def test_cors_middleware():
    response = client.options("/", headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"})
    assert response.status_code == 200
    # When allow_credentials=True, FastAPI reflects the origin instead of returning '*'
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"

def test_health_check_stub():
    # Assuming we might have a health check or just checking 404 on root
    response = client.get("/not-found")
    assert response.status_code == 404
