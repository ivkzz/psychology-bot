"""
Конфигурация Telegram бота.
Загружает настройки из переменных окружения.
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class BotSettings(BaseSettings):
    """
    Класс настроек Telegram бота.
    Все параметры загружаются из переменных окружения или .env файла.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Telegram Bot настройки
    TELEGRAM_BOT_TOKEN: str = Field(
        ...,
        description="Токен бота от BotFather"
    )

    # Backend API настройки
    BACKEND_API_URL: str = Field(
        default="http://backend:8000",
        description="URL Backend API для взаимодействия"
    )

    # Опциональные настройки
    TELEGRAM_WEBHOOK_URL: Optional[str] = None
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Database (если бот напрямую работает с БД)
    DATABASE_URL: Optional[str] = None

    # Redis (для кеширования и состояний)
    REDIS_URL: Optional[str] = None

    # Sentry для мониторинга ошибок
    SENTRY_DSN: Optional[str] = None

    # Scheduler настройки
    SCHEDULER_TIMEZONE: str = "Europe/Moscow"
    REMINDER_CHECK_INTERVAL_MINUTES: int = 5
    MORNING_TASK_TIME: str = "09:00"
    EVENING_REMINDER_TIME: str = "20:00"

    # Admin токен для планировщика (получение всех пользователей)
    ADMIN_TOKEN: Optional[str] = None

    # Admin Telegram IDs (через запятую) для тестовых команд
    ADMIN_TELEGRAM_IDS: str = ""


# Создаем глобальный экземпляр настроек
bot_settings = BotSettings()
