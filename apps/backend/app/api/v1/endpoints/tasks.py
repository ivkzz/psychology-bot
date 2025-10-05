"""
Task management endpoints.
Эндпоинты для работы с заданиями пользователей.
"""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.task import AssignmentResponse, AssignmentComplete
from app.services import task_service

router = APIRouter()


@router.get("/today", response_model=AssignmentResponse)
async def get_today_task(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить задание на сегодня.

    Если задание на сегодня еще не назначено, автоматически создает новое случайное задание.

    Args:
        current_user: Текущий пользователь
        db: Сессия базы данных

    Returns:
        AssignmentResponse: Задание на сегодня с данными упражнения
    """
    # Проверяем, есть ли задание на сегодня
    today_assignment = await task_service.get_today_task(db, current_user.id)

    # Если нет - создаем новое
    if not today_assignment:
        today_assignment = await task_service.assign_daily_task(db, current_user.id)

    return today_assignment


@router.post("/{assignment_id}/complete", response_model=AssignmentResponse)
async def complete_task(
    assignment_id: UUID,
    completion_data: AssignmentComplete,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Отметить задание как выполненное.

    Args:
        assignment_id: ID назначения
        completion_data: Данные о выполнении (ответ пользователя)
        current_user: Текущий пользователь
        db: Сессия базы данных

    Returns:
        AssignmentResponse: Обновленное назначение

    Raises:
        HTTPException 404: Если назначение не найдено
        HTTPException 403: Если назначение принадлежит другому пользователю
    """
    return await task_service.complete_task(
        db,
        user_id=current_user.id,
        assignment_id=assignment_id,
        answer_text=completion_data.answer_text
    )


@router.get("/history", response_model=list[AssignmentResponse])
async def get_task_history(
    limit: int = Query(10, ge=1, le=100, description="Количество записей"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить историю заданий пользователя.

    Args:
        limit: Максимальное количество записей (1-100)
        offset: Смещение для пагинации
        current_user: Текущий пользователь
        db: Сессия базы данных

    Returns:
        list[AssignmentResponse]: Список заданий с их данными
    """
    return await task_service.get_task_history(
        db,
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )
