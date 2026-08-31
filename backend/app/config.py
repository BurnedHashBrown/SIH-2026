import os
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Legal Metrology AI Compliance System"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security & JWT
    SECRET_KEY: str = "change-this-ultra-secure-secret-key-for-legal-metrology-compliance-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # Database
    DATABASE_URL: str = "sqlite:///./metrology.db"

    # CORS
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Storage Paths
    UPLOAD_DIR: str = "uploads"
    REPORT_DIR: str = "reports"
    MAX_UPLOAD_SIZE_MB: int = 10

    # AI & OCR Config
    OCR_ENGINE: str = "paddleocr"
    USE_MOCK_OCR_IF_UNAVAILABLE: bool = True

    # Seed Defaults
    SEED_ADMIN_EMAIL: str = "admin@metrology.gov.in"
    SEED_ADMIN_PASSWORD: str = "AdminPassword@2026"
    SEED_INSPECTOR_EMAIL: str = "inspector@metrology.gov.in"
    SEED_INSPECTOR_PASSWORD: str = "InspectorPassword@2026"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()

# Ensure critical directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.REPORT_DIR, exist_ok=True)
