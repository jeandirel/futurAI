import os
import pytest
from backend.app.core.settings import Settings

def test_settings_defaults():
    s = Settings()
    assert s.app_name == "OneClickQuiz Agents"
    assert s.postgres_dsn.startswith("postgresql://")

def test_settings_validation_error():
    with pytest.raises(ValueError):
        Settings(postgres_dsn="mysql://user:pass@localhost/db")

def test_settings_env_override(monkeypatch):
    monkeypatch.setenv("APP_NAME", "Test App")
    s = Settings()
    assert s.app_name == "Test App"
