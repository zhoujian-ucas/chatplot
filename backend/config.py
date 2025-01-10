import os
from pathlib import Path
from typing import List
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./chatplot.db")

    # Ollama
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")

    # Security
    CORS_ORIGINS: List[str] = json.loads(os.getenv("CORS_ORIGINS", '["http://localhost:3000"]'))

    # File Upload
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB
    ALLOWED_EXTENSIONS: List[str] = json.loads(
        os.getenv("ALLOWED_EXTENSIONS", '["csv", "xlsx", "xls", "json"]')
    )
    UPLOAD_DIR: Path = Path(os.getenv("UPLOAD_DIR", "./data/uploads"))

    def __init__(self):
        # Create upload directory if it doesn't exist
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    @property
    def ollama_generate_url(self) -> str:
        return f"{self.OLLAMA_BASE_URL}/api/generate"

    def is_allowed_file(self, filename: str) -> bool:
        return filename.split(".")[-1].lower() in self.ALLOWED_EXTENSIONS

# Create global settings instance
settings = Settings() 