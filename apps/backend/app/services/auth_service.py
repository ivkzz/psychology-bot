"""
Сервис для аутентификации и авторизации пользователей.
"""

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import user as user_crud
from app.schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, TokenResponse
from app.schemas.user import UserCreate
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_token


async def register_user(db: AsyncSession, data: RegisterRequest) -> RegisterResponse:
    """
    Регистрация нового пользователя в системе.

    Args:
        db: Сессия базы данных
        data: Данные для регистрации

    Returns:
        RegisterResponse: Данные пользователя и токены

    Raises:
        HTTPException: Если email уже зарегистрирован
    """
    # Проверяем, существует ли пользователь с таким email
    existing_user = await user_crud.get_by_email(db, data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегистрирован"
        )

    # Проверяем, существует ли пользователь с таким telegram_id (если указан)
    if data.telegram_id:
        existing_telegram_user = await user_crud.get_by_telegram_id(db, data.telegram_id)
        if existing_telegram_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким Telegram ID уже зарегистрирован"
            )

    # Создаем пользователя
    user_data = UserCreate(
        name=data.name,
        email=data.email,
        password=data.password,
        telegram_id=data.telegram_id
    )
    user = await user_crud.create(db, user_data)

    # Генерируем токены
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    # Формируем ответ
    from app.schemas.user import UserResponse
    return RegisterResponse(
        user=UserResponse.model_validate(user),
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


async def login(db: AsyncSession, data: LoginRequest) -> TokenResponse:
    """
    Вход пользователя в систему.

    Args:
        db: Сессия базы данных
        data: Данные для входа (email+password или telegram_id)

    Returns:
        TokenResponse: Токены доступа

    Raises:
        HTTPException: Если пользователь не найден или пароль неверный
    """
    # Вход через Telegram ID
    if data.telegram_id:
        user = await user_crud.get_by_telegram_id(db, data.telegram_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь с таким Telegram ID не найден",
                headers={"WWW-Authenticate": "Bearer"},
            )
    # Вход через email + password
    elif data.email and data.password:
        user = await user_crud.get_by_email(db, data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Проверяем, установлен ли пароль
        if not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Для этого пользователя не установлен пароль. Используйте вход через Telegram.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Проверяем пароль
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Необходимо указать либо telegram_id, либо email и password"
        )

    # Проверяем активность пользователя
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Аккаунт пользователя деактивирован"
        )

    # Генерируем токены
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> TokenResponse:
    """
    Обновление access token с использованием refresh token.

    Args:
        db: Сессия базы данных
        refresh_token: Refresh токен

    Returns:
        TokenResponse: Новые токены

    Raises:
        HTTPException: Если токен невалидный или пользователь не найден
    """
    # Проверяем refresh токен
    user_id = verify_token(refresh_token, token_type="refresh")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверяем существование пользователя
    from uuid import UUID
    user = await user_crud.get_by_id(db, UUID(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверяем активность пользователя
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Аккаунт пользователя деактивирован"
        )

    # Генерируем новые токены
    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )
