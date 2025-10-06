"""
Admin endpoints.
Эндпоинты для администраторов (CRUD шаблонов заданий, управление пользователями).
"""

from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.v1.dependencies import get_current_admin_user
from app.models.user import User
from app.models.task import TaskDifficulty
from app.schemas.user import UserResponse, UserProgress
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate, AssignmentResponse, AssignmentStatus
from app.crud import user as user_crud, task as task_crud, assignment as assignment_crud

router = APIRouter()


# ============ Управление пользователями ============

@router.get("/users", response_model=list[UserResponse])
async def get_all_users(
    skip: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(100, ge=1, le=100, description="Количество записей"),
    is_active: Optional[bool] = Query(None, description="Фильтр по активности"),
    _: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список всех пользователей (только для администраторов).

    Args:
        skip: Смещение для пагинации
        limit: Максимальное количество записей (1-100)
        is_active: Фильтр по статусу активности
        db: Сессия базы данных

    Returns:
        list[UserResponse]: Список пользователей
    """
    users = await user_crud.get_all(db, skip=skip, limit=limit, is_active=is_active)
    return [UserResponse.model_validate(u) for u in users]


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    _: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить данные пользователя по ID (только для администраторов).

    Args:
        user_id: ID пользователя
        db: Сессия базы данных

    Returns:
        UserResponse: Данные пользователя

    Raises:
        HTTPException 404: Если пользователь не найден
    """
    user = await user_crud.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return UserResponse.model_validate(user)


@router.get("/users/{user_id}/progress", response_model=UserProgress)
async def get_user_progress(
    user_id: UUID,
    _: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить статистику прогресса пользователя по ID (только для администраторов).

    Args:
        user_id: ID пользователя
        db: Сессия базы данных

    Returns:
        UserProgress: Статистика прогресса пользователя

    Raises:
        HTTPException 404: Если пользователь не найден
    """
    user = await user_crud.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    progress = await user_crud.get_user_progress(db, user_id)
    return progress


@router.get("/users/{user_id}/assignments", response_model=list[AssignmentResponse])
async def get_user_assignments(
    user_id: UUID,
    skip: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(100, ge=1, le=100, description="Количество записей"),
    status_filter: Optional[AssignmentStatus] = Query(None, alias="status", description="Фильтр по статусу"),
    _: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список заданий пользователя по ID (только для администраторов).

    Args:
        user_id: ID пользователя
        skip: Смещение для пагинации
        limit: Максимальное количество записей (1-100)
        status_filter: Фильтр по статусу (pending/completed)
        db: Сессия базы данных

    Returns:
        list[AssignmentResponse]: Список заданий пользователя

    Raises:
        HTTPException 404: Если пользователь не найден
    """
    user = await user_crud.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    assignments = await assignment_crud.get_user_assignments(
        db,
        user_id,
        skip=skip,
        limit=limit,
        status=status_filter
    )
    return [AssignmentResponse.model_validate(a) for a in assignments]


# ============ Управление шаблонами заданий ============

@router.get("/tasks/templates", response_model=list[TaskResponse])
async def get_task_templates(
    skip: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(100, ge=1, le=100, description="Количество записей"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    difficulty: Optional[TaskDifficulty] = Query(None, description="Фильтр по сложности"),
    _: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список всех шаблонов заданий (только для администраторов).

    Args:
        skip: Смещение для пагинации
        limit: Максимальное количество записей (1-100)
        category: Фильтр по категории
        difficulty: Фильтр по сложности
        db: Сессия базы данных

    Returns:
        list[TaskResponse]: Список шаблонов заданий
    """
    tasks = await task_crud.get_all(
        db,
        skip=skip,
        limit=limit,
        category=category,
        difficulty=difficulty
    )
    return [TaskResponse.model_validate(t) for t in tasks]


@router.post("/tasks/templates", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task_template(
    task_data: TaskCreate,
    _: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Создать новый шаблон задания (только для администраторов).

    Args:
        task_data: Данные для создания задания
        db: Сессия базы данных

    Returns:
        TaskResponse: Созданный шаблон задания
    """
    task = await task_crud.create(db, task_data)
    return TaskResponse.model_validate(task)


@router.patch("/tasks/templates/{task_id}", response_model=TaskResponse)
async def update_task_template(
    task_id: UUID,
    task_data: TaskUpdate,
    _: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Обновить шаблон задания (только для администраторов).

    Args:
        task_id: ID задания
        task_data: Данные для обновления
        db: Сессия базы данных

    Returns:
        TaskResponse: Обновленный шаблон задания

    Raises:
        HTTPException 404: Если задание не найдено
    """
    task = await task_crud.update(db, task_id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Шаблон задания не найден"
        )
    return TaskResponse.model_validate(task)


@router.delete("/tasks/templates/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_template(
    task_id: UUID,
    _: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Удалить шаблон задания (только для администраторов).

    Args:
        task_id: ID задания
        db: Сессия базы данных

    Raises:
        HTTPException 404: Если задание не найдено
    """
    deleted = await task_crud.delete(db, task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Шаблон задания не найден"
        )


@router.post("/users/{user_id}/assign-task", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def assign_task_to_user(
    user_id: UUID,
    task_id: UUID = Query(..., description="ID задания для назначения"),
    _: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Назначить задание пользователю (только для администраторов).

    Args:
        user_id: ID пользователя
        task_id: ID задания
        db: Сессия базы данных

    Returns:
        AssignmentResponse: Созданное назначение

    Raises:
        HTTPException 404: Если пользователь или задание не найдены
    """
    # Проверяем существование пользователя
    user = await user_crud.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    # Проверяем существование задания
    task = await task_crud.get_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задание не найдено"
        )

    # Создаем назначение
    assignment = await assignment_crud.create_daily_assignment(db, user_id, task_id)
    return AssignmentResponse.model_validate(assignment)
