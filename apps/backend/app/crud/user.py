"""
CRUD операции для работы с пользователями.
"""

from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime, date, timedelta
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, UserRole
from app.models.assignment import Assignment, AssignmentStatus
from app.schemas.user import UserCreate, UserUpdate, UserProgress
from app.core.security import get_password_hash


async def get_by_id(db: AsyncSession, user_id: UUID) -> Optional[User]:
    """
    Получить пользователя по ID.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя

    Returns:
        Optional[User]: Пользователь или None
    """
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Получить пользователя по email.

    Args:
        db: Сессия базы данных
        email: Email адрес

    Returns:
        Optional[User]: Пользователь или None
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_by_telegram_id(db: AsyncSession, telegram_id: int) -> Optional[User]:
    """
    Получить пользователя по Telegram ID.

    Args:
        db: Сессия базы данных
        telegram_id: ID пользователя в Telegram

    Returns:
        Optional[User]: Пользователь или None
    """
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, user_data: UserCreate) -> User:
    """
    Создать нового пользователя.

    Args:
        db: Сессия базы данных
        user_data: Данные для создания пользователя

    Returns:
        User: Созданный пользователь
    """
    user_dict = user_data.model_dump(exclude={"password"})

    # Хешируем пароль, если он предоставлен
    if user_data.password:
        user_dict["hashed_password"] = get_password_hash(user_data.password)

    user = User(**user_dict)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update(db: AsyncSession, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
    """
    Обновить данные пользователя.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя
        user_data: Данные для обновления

    Returns:
        Optional[User]: Обновленный пользователь или None
    """
    user = await get_by_id(db, user_id)
    if not user:
        return None

    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    user.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    return user


async def delete(db: AsyncSession, user_id: UUID) -> bool:
    """
    Удалить пользователя.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя

    Returns:
        bool: True если пользователь удален, False если не найден
    """
    user = await get_by_id(db, user_id)
    if not user:
        return False

    await db.delete(user)
    await db.commit()
    return True


async def get_user_progress(db: AsyncSession, user_id: UUID) -> UserProgress:
    """
    Получить статистику прогресса пользователя.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя

    Returns:
        UserProgress: Статистика пользователя
    """
    # Общее количество заданий
    total_tasks_query = await db.execute(
        select(func.count(Assignment.id)).where(Assignment.user_id == user_id)
    )
    total_tasks = total_tasks_query.scalar() or 0

    # Количество выполненных заданий
    completed_tasks_query = await db.execute(
        select(func.count(Assignment.id)).where(
            and_(
                Assignment.user_id == user_id,
                Assignment.status == AssignmentStatus.COMPLETED
            )
        )
    )
    completed_tasks = completed_tasks_query.scalar() or 0

    # Процент выполнения
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

    # Подсчет streak (дней подряд с выполненными заданиями)
    streak_days = await _calculate_streak_days(db, user_id)

    return UserProgress(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        completion_rate=round(completion_rate, 2),
        streak_days=streak_days
    )


async def _calculate_streak_days(db: AsyncSession, user_id: UUID) -> int:
    """
    Подсчитать количество дней подряд с выполненными заданиями.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя

    Returns:
        int: Количество дней подряд
    """
    # Получаем все выполненные задания, отсортированные по дате назначения
    result = await db.execute(
        select(Assignment.assigned_date)
        .where(
            and_(
                Assignment.user_id == user_id,
                Assignment.status == AssignmentStatus.COMPLETED
            )
        )
        .order_by(Assignment.assigned_date.desc())
    )
    completed_dates = [row[0] for row in result.all()]

    if not completed_dates:
        return 0

    # Проверяем, есть ли выполненное задание сегодня или вчера
    today = date.today()
    if completed_dates[0] not in [today, today - timedelta(days=1)]:
        return 0

    # Подсчитываем streak
    streak = 1
    current_date = completed_dates[0]

    for completed_date in completed_dates[1:]:
        expected_date = current_date - timedelta(days=1)
        if completed_date == expected_date:
            streak += 1
            current_date = completed_date
        else:
            break

    return streak


async def get_all(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None
) -> list[User]:
    """
    Получить список пользователей с пагинацией.

    Args:
        db: Сессия базы данных
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
        is_active: Фильтр по статусу активности (опционально)

    Returns:
        list[User]: Список пользователей
    """
    query = select(User)

    if is_active is not None:
        query = query.where(User.is_active == is_active)

    query = query.offset(skip).limit(limit).order_by(User.created_at.desc())

    result = await db.execute(query)
    return list(result.scalars().all())
