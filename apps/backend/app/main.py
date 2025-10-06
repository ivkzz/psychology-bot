"""
Главный модуль FastAPI приложения.
Точка входа для Backend API.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import close_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager для управления жизненным циклом приложения.
    """
    # Startup
    import sys
    print(f"🚀 Starting {settings.APP_NAME}", flush=True)
    sys.stdout.flush()
    print(f"🐛 Debug mode: {settings.DEBUG}", flush=True)
    sys.stdout.flush()

    # Запускаем планировщик задач (если настроен Telegram Bot Token)
    scheduler = None
    if settings.TELEGRAM_BOT_TOKEN:
        print("📋 TELEGRAM_BOT_TOKEN found, starting scheduler...", flush=True)
        sys.stdout.flush()
        from app.services.task_scheduler import task_scheduler
        task_scheduler.start()
        scheduler = task_scheduler
        print("✅ Task scheduler started successfully", flush=True)
        sys.stdout.flush()
        print(f"📅 Morning tasks: {settings.MORNING_TASK_TIME}, Evening reminders: {settings.EVENING_REMINDER_TIME}", flush=True)
        sys.stdout.flush()
    else:
        print("⚠️  TELEGRAM_BOT_TOKEN not set, scheduler disabled", flush=True)
        sys.stdout.flush()

    yield

    # Shutdown
    logger.info("Shutting down application...")

    if scheduler:
        scheduler.stop()
        logger.info("Task scheduler stopped")

    await close_db()


# Создаем экземпляр приложения FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="API для психолог-бота с поддержкой задач, пользователей и Telegram интеграции",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    """
    Корневой endpoint для проверки работоспособности API.
    """
    return {
        "message": "Psychology Bot API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint для мониторинга и Docker healthcheck.
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }


# Импорт и подключение роутеров
from app.api.v1.endpoints import auth, users, tasks, admin

app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["Users"])
app.include_router(tasks.router, prefix=f"{settings.API_V1_PREFIX}/tasks", tags=["Tasks"])
app.include_router(admin.router, prefix=f"{settings.API_V1_PREFIX}/admin", tags=["Admin"])
