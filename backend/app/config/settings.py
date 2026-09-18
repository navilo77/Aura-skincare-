from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    debug: bool = True

    database_url: str = ""
    database_echo: bool = False

    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""

    secret_key: str = "change-me"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    cors_origins: str = "http://localhost:3000"

    log_level: str = "INFO"

    n8n_webhook_url: str = "http://localhost:5678/webhook"

    ai_provider_api_key: str = ""
    gemini_api_key: str = ""
    google_api_key: str = ""


settings = Settings()
