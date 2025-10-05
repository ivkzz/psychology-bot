"""
Зависимости для FastAPI endpoints.
Используются для проверки аутентификации, получения текущего пользователя и т.д.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import verify_token

# Security схема для Bearer токена
security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Извлекает ID текущего пользователя из JWT токена.

    Args:
        credentials: Bearer токен из заголовка Authorization

    Returns:
        str: ID пользователя

    Raises:
        HTTPException: Если токен невалиден или отсутствует
    """
    token = credentials.credentials
    user_id = verify_token(token, token_type="access")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен авторизации",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Получает полный объект текущего пользователя из БД.

    Args:
        user_id: ID пользователя из токена
        db: Сессия БД

    Returns:
        User: Объект пользователя

    Raises:
        HTTPException: Если пользователь не найден
    """
    from uuid import UUID
    from app.crud import user as user_crud
    from app.models.user import User

    user = await user_crud.get_by_id(db, UUID(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user


async def get_current_active_user(
    current_user = Depends(get_current_user)
):
    """
    Проверяет, что текущий пользователь активен.

    Args:
        current_user: Текущий пользователь

    Returns:
        User: Активный пользователь

    Raises:
        HTTPException: Если пользователь неактивен
    """
    from app.models.user import User

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Аккаунт пользователя деактивирован"
        )
    return current_user


async def get_current_admin_user(
    current_user = Depends(get_current_active_user)
):
    """
    Проверяет, что текущий пользователь является администратором.

    Args:
        current_user: Текущий активный пользователь

    Returns:
        User: Пользователь с правами администратора

    Raises:
        HTTPException: Если пользователь не является администратором
    """
    from app.models.user import User, UserRole

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции"
        )
    return current_user
