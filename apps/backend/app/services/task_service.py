"""
Сервис для работы с заданиями и их назначениями.
"""

from typing import Optional
from uuid import UUID
from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import task as task_crud, assignment as assignment_crud
from app.models.assignment import Assignment
from app.models.task import TaskDifficulty
from app.schemas.task import AssignmentResponse, TaskResponse
from app.schemas.user import UserProgress


async def assign_daily_task(
    db: AsyncSession,
    user_id: UUID,
    category: Optional[str] = None,
    difficulty: Optional[TaskDifficulty] = None
) -> AssignmentResponse:
    """
    Назначить ежедневное задание пользователю.
    Если задание на сегодня уже существует, возвращает его.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя
        category: Категория задания (опционально)
        difficulty: Сложность задания (опционально)

    Returns:
        AssignmentResponse: Назначенное задание

    Raises:
        HTTPException: Если не найдено подходящих заданий
    """
    # Проверяем, есть ли уже задание на сегодня
    today_assignment = await assignment_crud.get_today_assignment(db, user_id)
    if today_assignment:
        return AssignmentResponse.model_validate(today_assignment)

    # Получаем случайное задание
    task = await task_crud.get_random_task(db, category=category, difficulty=difficulty)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найдено подходящих заданий"
        )

    # Создаем назначение
    assignment = await assignment_crud.create_daily_assignment(
        db,
        user_id=user_id,
        task_id=task.id
    )

    return AssignmentResponse.model_validate(assignment)


async def complete_task(
    db: AsyncSession,
    user_id: UUID,
    assignment_id: UUID,
    answer_text: Optional[str] = None
) -> AssignmentResponse:
    """
    Отметить задание как выполненное.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя
        assignment_id: ID назначения
        answer_text: Текстовый ответ пользователя (опционально)

    Returns:
        AssignmentResponse: Обновленное назначение

    Raises:
        HTTPException: Если назначение не найдено или принадлежит другому пользователю
    """
    # Получаем назначение
    assignment = await assignment_crud.get_by_id(db, assignment_id)
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Назначение не найдено"
        )

    # Проверяем, что назначение принадлежит пользователю
    if assignment.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этому назначению"
        )

    # Отмечаем как выполненное
    updated_assignment = await assignment_crud.mark_as_completed(
        db,
        assignment_id=assignment_id,
        answer_text=answer_text
    )

    return AssignmentResponse.model_validate(updated_assignment)


async def get_user_progress(db: AsyncSession, user_id: UUID) -> UserProgress:
    """
    Получить статистику прогресса пользователя.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя

    Returns:
        UserProgress: Статистика пользователя
    """
    from app.crud import user as user_crud
    return await user_crud.get_user_progress(db, user_id)


async def get_task_history(
    db: AsyncSession,
    user_id: UUID,
    limit: int = 10,
    offset: int = 0
) -> list[AssignmentResponse]:
    """
    Получить историю заданий пользователя.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя
        limit: Максимальное количество записей
        offset: Смещение для пагинации

    Returns:
        list[AssignmentResponse]: Список назначений с заданиями
    """
    assignments = await assignment_crud.get_user_assignments(
        db,
        user_id=user_id,
        skip=offset,
        limit=limit
    )

    return [AssignmentResponse.model_validate(a) for a in assignments]


async def get_today_task(db: AsyncSession, user_id: UUID) -> Optional[AssignmentResponse]:
    """
    Получить задание на сегодня, если оно существует.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя

    Returns:
        Optional[AssignmentResponse]: Задание на сегодня или None
    """
    assignment = await assignment_crud.get_today_assignment(db, user_id)
    if not assignment:
        return None

    return AssignmentResponse.model_validate(assignment)
