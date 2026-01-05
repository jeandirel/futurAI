from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "OneClickQuiz Agents"
    version: str = "0.1.0"
    redis_url: str = "redis://localhost:6379/0"
    postgres_dsn: str = "postgresql://user:password@localhost:5432/oneclickquiz"
    allowed_origins: List[str] = ["*"]
    use_llm: bool = False
    hf_api_token: str | None = None
    hf_model_id: str | None = None
    hf_timeout: int = 30
    hf_api_base: str = "https://router.huggingface.co"
    hf_fallback_model: str = "HuggingFaceH4/zephyr-7b-beta"
    use_toxicity: bool = False
    toxicity_model_id: str | None = None
    toxicity_api_base: str = "https://router.huggingface.co"
    toxicity_threshold: float = 0.6

    # Gemini Configuration
    llm_provider: str = "hf"  # "hf", "gemini", "openrouter"
    google_api_key: str | None = None
    google_model_id: str = "gemini-1.5-flash"

    # OpenRouter Configuration
    openrouter_api_key: str | None = None
    openrouter_model: str = "meta-llama/llama-3.1-70b-instruct"

    @field_validator("postgres_dsn")
    @classmethod
    def validate_postgres(cls, v: str) -> str:
        if not v.lower().startswith("postgresql://"):
            raise ValueError("POSTGRES_DSN must start with postgresql://")
        return v

    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"


settings = Settings()
