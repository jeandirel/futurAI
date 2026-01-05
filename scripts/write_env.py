from pathlib import Path

content = """POSTGRES_DSN=postgresql://postgres:pass@localhost:5432/oneclickquiz
REDIS_URL=redis://localhost:6379/0
APP_NAME=OneClickQuiz Agents
VERSION=0.1.0
ALLOWED_ORIGINS=["*"]
USE_LLM=True
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=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
OPENROUTER_MODEL=meta-llama/llama-3.1-70b-instruct
HF_TIMEOUT=60
"""

path = Path("config/.env")
path.parent.mkdir(parents=True, exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Wrote {path}")
