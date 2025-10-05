"""
Сервис для отправки уведомлений пользователям.
Заглушка для будущей интеграции с Telegram и другими каналами.
"""

from typing import Optional
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


async def send_notification(
    user_id: UUID,
    message: str,
    notification_type: str = "general"
) -> bool:
    """
    Отправить уведомление пользователю.

    Args:
        user_id: ID пользователя
        message: Текст сообщения
        notification_type: Тип уведомления (general, task_reminder, etc.)

    Returns:
        bool: True если уведомление отправлено успешно

    Note:
        Текущая реализация - заглушка. В будущем будет интегрирована
        с Telegram Bot API для отправки реальных уведомлений.
    """
    logger.info(
        f"[NOTIFICATION] User: {user_id}, Type: {notification_type}, Message: {message}"
    )

    # TODO: Интеграция с Telegram Bot
    # - Получить telegram_id пользователя из БД
    # - Отправить сообщение через Telegram Bot API
    # - Обработать ошибки отправки

    return True


async def send_task_reminder(user_id: UUID, task_title: str) -> bool:
    """
    Отправить напоминание о выполнении задания.

    Args:
        user_id: ID пользователя
        task_title: Название задания

    Returns:
        bool: True если напоминание отправлено
    """
    message = f"Напоминание: у вас есть невыполненное задание - {task_title}"
    return await send_notification(
        user_id=user_id,
        message=message,
        notification_type="task_reminder"
    )


async def send_daily_task_notification(
    user_id: UUID,
    task_title: str,
    task_description: str
) -> bool:
    """
    Отправить уведомление о новом ежедневном задании.

    Args:
        user_id: ID пользователя
        task_title: Название задания
        task_description: Описание задания

    Returns:
        bool: True если уведомление отправлено
    """
    message = (
        f"Доброе утро! Ваше задание на сегодня:\n\n"
        f"{task_title}\n\n"
        f"{task_description}"
    )
    return await send_notification(
        user_id=user_id,
        message=message,
        notification_type="daily_task"
    )


async def send_completion_congratulation(
    user_id: UUID,
    streak_days: int
) -> bool:
    """
    Отправить поздравление с выполнением задания.

    Args:
        user_id: ID пользователя
        streak_days: Количество дней подряд с выполненными заданиями

    Returns:
        bool: True если поздравление отправлено
    """
    message = f"Отлично! Задание выполнено. Ваша серия: {streak_days} дней подряд!"
    return await send_notification(
        user_id=user_id,
        message=message,
        notification_type="completion"
    )
