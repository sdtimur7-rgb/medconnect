from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    # Database
    DB_PASSWORD: str = Field(default="strongpassword123")
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://medconnect:strongpassword123@postgres/medconnect"
    )
    
    # Redis
    REDIS_URL: str = Field(default="redis://redis:6379/0")
    CELERY_BROKER_URL: str = Field(default="redis://redis:6379/0")
    CELERY_RESULT_BACKEND: str = Field(default="redis://redis:6379/0")
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str = Field(default="")
    ADMIN_TELEGRAM_ID: Optional[int] = Field(default=None)
    
    # Anthropic Claude API
    ANTHROPIC_API_KEY: str = Field(default="")
    ANTHROPIC_MODEL: str = Field(default="claude-sonnet-4-20250514")
    
    # SMS Center API
    SMSC_LOGIN: str = Field(default="")
    SMSC_PASSWORD: str = Field(default="")
    SMSC_ENABLED: bool = Field(default=True)
    
    # Chatwoot
    CHATWOOT_API_URL: str = Field(default="http://chatwoot:3000")
    CHATWOOT_API_TOKEN: str = Field(default="")
    CHATWOOT_ACCOUNT_ID: str = Field(default="1")
    CHATWOOT_SECRET_KEY: str = Field(default="replace_with_random_secret")
    CHATWOOT_FRONTEND_URL: str = Field(default="http://localhost:3000")
    
    # Application
    APP_NAME: str = Field(default="MedConnect")
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO")
    
    # API
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)
    
    # Monitoring
    SENTRY_DSN: Optional[str] = Field(default=None)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
