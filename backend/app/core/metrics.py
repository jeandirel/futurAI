from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST  # type: ignore

# RAG
rag_requests = Counter("rag_requests_total", "Total RAG search requests")
rag_latency = Histogram("rag_latency_seconds", "Latency of RAG search")

# LLM
llm_requests = Counter("llm_requests_total", "Total LLM generation attempts", ["status", "model"])
llm_latency = Histogram("llm_latency_seconds", "Latency of LLM generation")

# Healing
healing_requests = Counter("healing_requests_total", "Total healing attempts")
healing_latency = Histogram("healing_latency_seconds", "Latency of healing attempts")

# Toxicity
toxicity_checks = Counter("toxicity_checks_total", "Total toxicity checks")
toxicity_blocked = Counter("toxicity_blocked_total", "Items blocked by toxicity")

# Jobs
jobs_created = Counter("jobs_created_total", "Jobs created")
jobs_completed = Counter("jobs_completed_total", "Jobs completed")
jobs_failed = Counter("jobs_failed_total", "Jobs failed")
