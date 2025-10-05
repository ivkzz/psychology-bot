"""
Конфигурация приложения Backend.
Загружает настройки из переменных окружения.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn, field_validator


class Settings(BaseSettings):
    """
    Класс настроек приложения.
    Все параметры загружаются из переменных окружения или .env файла.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Основные настройки приложения
    APP_NAME: str = "Psychology Bot API"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # База данных
    DATABASE_URL: PostgresDsn = Field(
        ...,
        description="URL подключения к PostgreSQL базе данных"
    )

    # Безопасность и аутентификация
    SECRET_KEY: str = Field(
        ...,
        min_length=32,
        description="Секретный ключ для JWT токенов (минимум 32 символа)"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS настройки
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000"
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Преобразует строку с CORS origins в список."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # Опциональные настройки
    SENTRY_DSN: Optional[str] = None
    REDIS_URL: Optional[str] = None
    LOG_LEVEL: str = "INFO"

    # Telegram Bot (для интеграции)
    TELEGRAM_BOT_TOKEN: Optional[str] = None

    # Seed данные для первого администратора
    ADMIN_EMAIL: str = Field(
        default="klevin.ivan.ivk@yandex.ru",
        description="Email администратора для первоначального seed"
    )
    ADMIN_PASSWORD: str = Field(
        default="admin123",
        description="Пароль администратора (рекомендуется изменить в production)"
    )
    ADMIN_NAME: str = Field(
        default="Admin",
        description="IVK"
    )


# Создаем глобальный экземпляр настроек
settings = Settings()
