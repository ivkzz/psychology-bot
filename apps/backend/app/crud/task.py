"""
CRUD операции для работы с заданиями (шаблонами упражнений).
"""

from typing import Optional
from uuid import UUID
import random
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task, TaskDifficulty
from app.schemas.task import TaskCreate, TaskUpdate


async def get_by_id(db: AsyncSession, task_id: UUID) -> Optional[Task]:
    """
    Получить задание по ID.

    Args:
        db: Сессия базы данных
        task_id: ID задания

    Returns:
        Optional[Task]: Задание или None
    """
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def get_all(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    difficulty: Optional[TaskDifficulty] = None
) -> list[Task]:
    """
    Получить список заданий с пагинацией и фильтрацией.

    Args:
        db: Сессия базы данных
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
        category: Фильтр по категории (опционально)
        difficulty: Фильтр по сложности (опционально)

    Returns:
        list[Task]: Список заданий
    """
    query = select(Task)

    if category:
        query = query.where(Task.category == category)
    if difficulty:
        query = query.where(Task.difficulty == difficulty)

    query = query.offset(skip).limit(limit).order_by(Task.created_at.desc())

    result = await db.execute(query)
    return list(result.scalars().all())


async def create(db: AsyncSession, task_data: TaskCreate) -> Task:
    """
    Создать новое задание.

    Args:
        db: Сессия базы данных
        task_data: Данные для создания задания

    Returns:
        Task: Созданное задание
    """
    task = Task(**task_data.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def update(db: AsyncSession, task_id: UUID, task_data: TaskUpdate) -> Optional[Task]:
    """
    Обновить задание.

    Args:
        db: Сессия базы данных
        task_id: ID задания
        task_data: Данные для обновления

    Returns:
        Optional[Task]: Обновленное задание или None
    """
    task = await get_by_id(db, task_id)
    if not task:
        return None

    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)
    return task


async def delete(db: AsyncSession, task_id: UUID) -> bool:
    """
    Удалить задание.

    Args:
        db: Сессия базы данных
        task_id: ID задания

    Returns:
        bool: True если задание удалено, False если не найдено
    """
    task = await get_by_id(db, task_id)
    if not task:
        return False

    await db.delete(task)
    await db.commit()
    return True


async def get_random_task(
    db: AsyncSession,
    category: Optional[str] = None,
    difficulty: Optional[TaskDifficulty] = None
) -> Optional[Task]:
    """
    Получить случайное задание с опциональной фильтрацией.

    Args:
        db: Сессия базы данных
        category: Фильтр по категории (опционально)
        difficulty: Фильтр по сложности (опционально)

    Returns:
        Optional[Task]: Случайное задание или None
    """
    query = select(Task)

    if category:
        query = query.where(Task.category == category)
    if difficulty:
        query = query.where(Task.difficulty == difficulty)

    # Получаем количество подходящих заданий
    count_query = select(func.count()).select_from(query.alias())
    count_result = await db.execute(count_query)
    total_count = count_result.scalar()

    if not total_count:
        return None

    # Выбираем случайное смещение
    random_offset = random.randint(0, total_count - 1)
    query = query.offset(random_offset).limit(1)

    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_categories(db: AsyncSession) -> list[str]:
    """
    Получить список всех уникальных категорий заданий.

    Args:
        db: Сессия базы данных

    Returns:
        list[str]: Список категорий
    """
    result = await db.execute(select(Task.category).distinct())
    return [row[0] for row in result.all()]
