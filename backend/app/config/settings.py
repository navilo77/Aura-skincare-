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

    secret_key: str = ""
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    cors_origins: str = "http://localhost:3000"

    log_level: str = "INFO"

    redis_url: str = "redis://localhost:6379/0"

    n8n_webhook_url: str = "http://localhost:5678/webhook"

    ai_provider_api_key: str = ""
    gemini_api_key: str = ""
    google_api_key: str = ""

    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""

    sendgrid_api_key: str = ""
    sendgrid_from_email: str = ""
    sendgrid_from_name: str = ""

    aws_region: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    s3_bucket: str = ""

    enable_s3: bool = False
    enable_email: bool = False
    enable_payment: bool = False

    ollama_url: str = "http://localhost:11434"
    ollama_embedding_model: str = "bge-m3"


settings = Settings()
