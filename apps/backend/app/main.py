"""
Главный модуль FastAPI приложения.
Точка входа для Backend API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import close_db


# Создаем экземпляр приложения FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="API для психолог-бота с поддержкой задач, пользователей и Telegram интеграции",
    debug=settings.DEBUG,
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Событие запуска приложения.
    Инициализирует подключения и ресурсы.
    """
    print(f"Starting {settings.APP_NAME}")
    print(f"Debug mode: {settings.DEBUG}")
    # Здесь можно добавить дополнительную инициализацию
    # Например, подключение к Redis, проверка БД и т.д.


@app.on_event("shutdown")
async def shutdown_event():
    """
    Событие остановки приложения.
    Закрывает подключения и освобождает ресурсы.
    """
    print("Shutting down application...")
    await close_db()


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
