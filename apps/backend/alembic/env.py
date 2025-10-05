"""
Alembic environment configuration.
Используется для выполнения миграций базы данных.
"""

import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import os
import sys

# Добавляем корневую директорию приложения в путь Python
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.core.database import Base

# Импортируем все модели, чтобы Alembic их увидел
from app.models.user import User
from app.models.task import Task
from app.models.assignment import Assignment

# Alembic Config object
config = context.config

# Интерпретируем конфигурацию логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные моделей для автогенерации миграций
target_metadata = Base.metadata

# Получаем DATABASE_URL из переменных окружения
database_url = str(settings.DATABASE_URL).replace(
    "postgresql://", "postgresql+asyncpg://"
)


def run_migrations_offline() -> None:
    """
    Выполнение миграций в 'offline' режиме.
    Не требует подключения к БД, генерирует SQL скрипты.
    """
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Выполняет миграции с использованием существующего подключения.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Асинхронное выполнение миграций.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = database_url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Выполнение миграций в 'online' режиме.
    Требует активного подключения к БД.
    """
    asyncio.run(run_async_migrations())


# Определяем режим работы (online/offline)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
