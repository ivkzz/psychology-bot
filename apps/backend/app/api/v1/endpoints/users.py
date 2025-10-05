"""
User management endpoints.
Эндпоинты для управления пользователями.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserProgress
from app.crud import user as user_crud
from app.services import task_service

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: User = Depends(get_current_active_user)
):
    """
    Получить данные текущего пользователя.

    Args:
        current_user: Текущий аутентифицированный пользователь

    Returns:
        UserResponse: Данные пользователя
    """
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить данные текущего пользователя.

    Args:
        user_data: Данные для обновления
        current_user: Текущий пользователь
        db: Сессия базы данных

    Returns:
        UserResponse: Обновленные данные пользователя

    Raises:
        HTTPException 400: Если email уже используется другим пользователем
    """
    # Проверяем, не занят ли новый email другим пользователем
    if user_data.email:
        existing_user = await user_crud.get_by_email(db, user_data.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email уже используется другим пользователем"
            )

    # Обновляем пользователя
    updated_user = await user_crud.update(db, current_user.id, user_data)
    return UserResponse.model_validate(updated_user)


@router.get("/me/progress", response_model=UserProgress)
async def get_user_progress(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить статистику прогресса текущего пользователя.

    Args:
        current_user: Текущий пользователь
        db: Сессия базы данных

    Returns:
        UserProgress: Статистика выполнения заданий
    """
    return await task_service.get_user_progress(db, current_user.id)
