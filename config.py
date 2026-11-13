from functools import lru_cache
from pydantic import SecretStr
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str |None=None
    REDIS_URL:str |None=None
    QDRANT_URL:str |None=None
    PHOENIX_ENDPOINT:str |None=None
    POSTGRES_PASSWORD:str |None=None
    POSTGRES_USER:str |None=None
    POSTGRES_DB:str |None=None
    TEST_DATABASE_URL:str |None=None

    MAX_UPLOAD_FILE_SIZE_MB: int = 50
    ALLOWED_FILE_EXTENSIONS:list[str]=[".pdf",".docx",".txt"]

    cohere_api_key: SecretStr
    cohere_embedding_model: str = "embed-v5.0-fast"
    cohere_embedding_dimensions: int = 1024

    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def get_settings():
    return Settings()