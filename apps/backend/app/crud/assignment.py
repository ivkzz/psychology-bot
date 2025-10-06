"""
CRUD операции для работы с назначениями заданий пользователям.
"""

from typing import Optional
from uuid import UUID
from datetime import datetime, date
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.assignment import Assignment, AssignmentStatus
from app.schemas.task import AssignmentCreate, AssignmentUpdate


async def get_by_id(db: AsyncSession, assignment_id: UUID) -> Optional[Assignment]:
    """
    Получить назначение по ID с загрузкой связанного задания.

    Args:
        db: Сессия базы данных
        assignment_id: ID назначения

    Returns:
        Optional[Assignment]: Назначение с загруженным заданием или None
    """
    result = await db.execute(
        select(Assignment)
        .options(selectinload(Assignment.task))
        .where(Assignment.id == assignment_id)
    )
    return result.scalar_one_or_none()


async def get_user_assignments(
    db: AsyncSession,
    user_id: UUID,
    skip: int = 0,
    limit: int = 100,
    status: Optional[AssignmentStatus] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> list[Assignment]:
    """
    Получить список назначений пользователя с фильтрацией.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя
        skip: Количество записей для пропуска
        limit: Максимальное количество записей
        status: Фильтр по статусу (опционально)
        start_date: Начальная дата (опционально)
        end_date: Конечная дата (опционально)

    Returns:
        list[Assignment]: Список назначений с загруженными заданиями
    """
    query = select(Assignment).options(selectinload(Assignment.task)).where(
        Assignment.user_id == user_id
    )

    if status:
        query = query.where(Assignment.status == status)
    if start_date:
        query = query.where(Assignment.assigned_date >= start_date)
    if end_date:
        query = query.where(Assignment.assigned_date <= end_date)

    query = query.offset(skip).limit(limit).order_by(Assignment.assigned_date.desc())

    result = await db.execute(query)
    return list(result.scalars().all())


async def get_today_assignment(db: AsyncSession, user_id: UUID) -> Optional[Assignment]:
    """
    Получить назначение пользователя на сегодня (только PENDING).

    Args:
        db: Сессия базы данных
        user_id: ID пользователя

    Returns:
        Optional[Assignment]: Назначение на сегодня с загруженным заданием или None
    """
    today = date.today()
    result = await db.execute(
        select(Assignment)
        .options(selectinload(Assignment.task))
        .where(
            and_(
                Assignment.user_id == user_id,
                Assignment.assigned_date == today,
                Assignment.status == AssignmentStatus.PENDING
            )
        )
        .order_by(Assignment.created_at.asc())  # Берём самое раннее задание
        .limit(1)
    )
    return result.scalar_one_or_none()


async def has_completed_task_today(db: AsyncSession, user_id: UUID) -> bool:
    """
    Проверить, выполнил ли пользователь хотя бы одно задание сегодня.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя

    Returns:
        bool: True если есть выполненное задание на сегодня
    """
    today = date.today()
    result = await db.execute(
        select(Assignment)
        .where(
            and_(
                Assignment.user_id == user_id,
                Assignment.assigned_date == today,
                Assignment.status == AssignmentStatus.COMPLETED
            )
        )
        .limit(1)
    )
    return result.scalar_one_or_none() is not None


async def get_next_pending_assignment(db: AsyncSession, user_id: UUID) -> Optional[Assignment]:
    """
    Получить следующее задание из очереди pending (assigned_date = NULL).

    Args:
        db: Сессия базы данных
        user_id: ID пользователя

    Returns:
        Optional[Assignment]: Первое pending задание из очереди или None
    """
    result = await db.execute(
        select(Assignment)
        .options(selectinload(Assignment.task))
        .where(
            and_(
                Assignment.user_id == user_id,
                Assignment.assigned_date.is_(None),
                Assignment.status == AssignmentStatus.PENDING
            )
        )
        .order_by(Assignment.created_at.asc())  # FIFO - первое созданное
        .limit(1)
    )
    return result.scalar_one_or_none()


async def assign_pending_to_date(
    db: AsyncSession,
    assignment_id: UUID,
    target_date: date
) -> Assignment:
    """
    Назначить pending задание на конкретную дату.

    Args:
        db: Сессия базы данных
        assignment_id: ID назначения
        target_date: Целевая дата назначения

    Returns:
        Assignment: Обновленное назначение с датой
    """
    assignment = await get_by_id(db, assignment_id)
    if not assignment:
        raise ValueError("Assignment not found")

    assignment.assigned_date = target_date
    await db.commit()
    await db.refresh(assignment)

    # Перезагружаем с заданием
    result = await db.execute(
        select(Assignment)
        .options(selectinload(Assignment.task))
        .where(Assignment.id == assignment.id)
    )
    return result.scalar_one()


async def create_daily_assignment(
    db: AsyncSession,
    user_id: UUID,
    task_id: UUID,
    assigned_date: Optional[date] = None
) -> Assignment:
    """
    Создать назначение задания пользователю.

    Если assigned_date = None, задание попадает в очередь pending (будет назначено при запросе).
    Если указана дата, проверяем существование назначения на эту дату.

    Args:
        db: Сессия базы данных
        user_id: ID пользователя
        task_id: ID задания
        assigned_date: Дата назначения (None = в очередь, иначе конкретная дата)

    Returns:
        Assignment: Созданное назначение с загруженным заданием
    """
    # Если указана конкретная дата, проверяем существование
    if assigned_date is not None:
        existing = await db.execute(
            select(Assignment)
            .where(
                and_(
                    Assignment.user_id == user_id,
                    Assignment.assigned_date == assigned_date
                )
            )
        )
        existing_assignment = existing.scalar_one_or_none()

        # Если уже есть задание на эту дату, возвращаем его
        if existing_assignment:
            result = await db.execute(
                select(Assignment)
                .options(selectinload(Assignment.task))
                .where(Assignment.id == existing_assignment.id)
            )
            return result.scalar_one()

    assignment_data = AssignmentCreate(
        user_id=user_id,
        task_id=task_id,
        assigned_date=assigned_date  # Может быть None для pending заданий
    )

    assignment = Assignment(**assignment_data.model_dump())
    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)

    # Загружаем связанное задание
    result = await db.execute(
        select(Assignment)
        .options(selectinload(Assignment.task))
        .where(Assignment.id == assignment.id)
    )
    return result.scalar_one()


async def mark_as_completed(
    db: AsyncSession,
    assignment_id: UUID,
    answer_text: Optional[str] = None
) -> Optional[Assignment]:
    """
    Отметить задание как выполненное.

    Args:
        db: Сессия базы данных
        assignment_id: ID назначения
        answer_text: Текстовый ответ пользователя (опционально)

    Returns:
        Optional[Assignment]: Обновленное назначение или None
    """
    assignment = await get_by_id(db, assignment_id)
    if not assignment:
        return None

    # Проверяем, что задание еще не выполнено
    if assignment.status == AssignmentStatus.COMPLETED:
        # Если уже выполнено, просто возвращаем с заданием
        result = await db.execute(
            select(Assignment)
            .options(selectinload(Assignment.task))
            .where(Assignment.id == assignment.id)
        )
        return result.scalar_one()

    assignment.status = AssignmentStatus.COMPLETED
    assignment.completed_at = datetime.utcnow()
    if answer_text:
        assignment.answer_text = answer_text

    await db.commit()
    await db.refresh(assignment)

    # Перезагружаем с заданием
    result = await db.execute(
        select(Assignment)
        .options(selectinload(Assignment.task))
        .where(Assignment.id == assignment.id)
    )
    return result.scalar_one()


async def update(
    db: AsyncSession,
    assignment_id: UUID,
    assignment_data: AssignmentUpdate
) -> Optional[Assignment]:
    """
    Обновить назначение.

    Args:
        db: Сессия базы данных
        assignment_id: ID назначения
        assignment_data: Данные для обновления

    Returns:
        Optional[Assignment]: Обновленное назначение или None
    """
    assignment = await get_by_id(db, assignment_id)
    if not assignment:
        return None

    update_data = assignment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assignment, field, value)

    await db.commit()
    await db.refresh(assignment)

    # Перезагружаем с заданием
    result = await db.execute(
        select(Assignment)
        .options(selectinload(Assignment.task))
        .where(Assignment.id == assignment.id)
    )
    return result.scalar_one()


async def delete(db: AsyncSession, assignment_id: UUID) -> bool:
    """
    Удалить назначение.

    Args:
        db: Сессия базы данных
        assignment_id: ID назначения

    Returns:
        bool: True если назначение удалено, False если не найдено
    """
    assignment = await get_by_id(db, assignment_id)
    if not assignment:
        return False

    await db.delete(assignment)
    await db.commit()
    return True
