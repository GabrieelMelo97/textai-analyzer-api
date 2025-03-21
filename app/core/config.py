import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Text Analysis API"
    PROJECT_VERSION: str = "1.0.0"
    
    # API Keys
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY")
    API_KEY: str = os.getenv("API_KEY")
    
    # Model Settings
    MODEL_NAME: str = os.getenv("MODEL_NAME", "deepseek-chat")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0"))
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # Cache Settings
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour in seconds
    MAX_CACHE_ITEMS: int = int(os.getenv("MAX_CACHE_ITEMS", "1000"))
    
    # Validation
    MAX_TEXT_LENGTH: int = int(os.getenv("MAX_TEXT_LENGTH", "5000"))
    MIN_TEXT_LENGTH: int = int(os.getenv("MIN_TEXT_LENGTH", "10"))
    
    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY must be set in environment variables")
        if self.API_KEY == "your-api-key-here":
            raise ValueError("API_KEY must be set in environment variables")

settings = Settings()