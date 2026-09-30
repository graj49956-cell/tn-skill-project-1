from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "EduGenie"
    app_description: str = "Google Gemini Powered Learning Assistant"
    environment: str = "development"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"
    gemini_timeout_seconds: float = 60.0
    gemini_max_retries: int = 2
    explanation_provider: str = "gemini"
    explanation_model: str = "MBZUAI/LaMini-Flan-T5-783M"
    local_max_new_tokens: int = 150
    local_temperature: float = 0.7
    local_top_k: int = 50
    local_top_p: float = 0.95
    cors_origins: str = "http://127.0.0.1:8000,http://localhost:8000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8",
                                      case_sensitive=False, extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
