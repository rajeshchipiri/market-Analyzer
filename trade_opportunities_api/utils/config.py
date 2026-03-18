from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Trade Opportunities API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Optional API Keys
    GEMINI_API_KEY: str | None = None
    
    # Rate Limiting & Performance
    RATE_LIMIT_LOGIN: str = "10 per minute"
    RATE_LIMIT_ANALYZE: str = "5 per minute"
    CACHE_TTL: int = 3600  # Default 1 hour
    
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
