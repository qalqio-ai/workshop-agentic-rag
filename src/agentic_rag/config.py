from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    model_provider: str = os.getenv("MODEL_PROVIDER", "mock").lower()
    model_name: str = os.getenv("MODEL_NAME", "gpt-4.1-mini")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    qdrant_path: str = os.getenv("QDRANT_PATH", "./qdrant_storage")
    session_db_path: str = os.getenv("SESSION_DB_PATH", "./local-data/sessions.sqlite3")
    evidence_threshold: float = float(os.getenv("EVIDENCE_THRESHOLD", "0.15"))
    session_ttl_seconds: int = int(os.getenv("SESSION_TTL_SECONDS", "3600"))
    vector_size: int = 384


settings = Settings()
