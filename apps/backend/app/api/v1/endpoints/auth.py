"""
Authentication endpoints.
Эндпоинты для регистрации, входа, обновления токенов.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
)
from app.services import auth_service

router = APIRouter()


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Регистрация нового пользователя.

    Создает нового пользователя в системе и возвращает данные пользователя с токенами доступа.

    Args:
        data: Данные для регистрации (имя, email, пароль, telegram_id)
        db: Сессия базы данных

    Returns:
        RegisterResponse: Данные пользователя и токены (access, refresh)

    Raises:
        HTTPException 400: Если пользователь с таким email или telegram_id уже существует
    """
    return await auth_service.register_user(db, data)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Вход пользователя в систему.

    Проверяет учетные данные и возвращает токены доступа.

    Args:
        data: Данные для входа (email, пароль)
        db: Сессия базы данных

    Returns:
        TokenResponse: Токены доступа (access, refresh)

    Raises:
        HTTPException 401: Если email или пароль неверные
        HTTPException 403: Если аккаунт деактивирован
    """
    return await auth_service.login(db, data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: RefreshRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновление access token с использованием refresh token.

    Args:
        data: Refresh токен
        db: Сессия базы данных

    Returns:
        TokenResponse: Новые токены доступа (access, refresh)

    Raises:
        HTTPException 401: Если refresh token невалидный или пользователь не найден
        HTTPException 403: Если аккаунт деактивирован
    """
    return await auth_service.refresh_access_token(db, data.refresh_token)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    """
    Выход пользователя из системы.

    Note:
        В текущей реализации JWT токены не могут быть отозваны на сервере.
        Клиент должен удалить токены локально.
        В будущем можно реализовать blacklist токенов через Redis.

    Returns:
        dict: Сообщение об успешном выходе
    """
    return {"message": "Успешный выход из системы"}
