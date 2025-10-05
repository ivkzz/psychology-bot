"""
Общие утилиты, используемые во всех частях проекта.
"""

from datetime import datetime, timedelta
from typing import Optional
import re


def is_valid_email(email: str) -> bool:
    """
    Проверяет валидность email адреса.

    Args:
        email: Email адрес для проверки

    Returns:
        bool: True если email валиден
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_telegram_id(telegram_id: int) -> bool:
    """
    Проверяет валидность Telegram ID.

    Args:
        telegram_id: Telegram ID пользователя

    Returns:
        bool: True если ID валиден
    """
    return telegram_id > 0 and telegram_id < 10**15


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Форматирует datetime объект в строку.

    Args:
        dt: Datetime объект
        format_str: Формат вывода

    Returns:
        str: Отформатированная строка
    """
    return dt.strftime(format_str)


def get_deadline_from_now(days: int = 7) -> datetime:
    """
    Вычисляет дедлайн от текущего момента.

    Args:
        days: Количество дней

    Returns:
        datetime: Дедлайн
    """
    return datetime.utcnow() + timedelta(days=days)


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Обрезает строку до указанной длины.

    Args:
        text: Исходная строка
        max_length: Максимальная длина
        suffix: Суффикс для обрезанной строки

    Returns:
        str: Обрезанная строка
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def sanitize_html(text: str) -> str:
    """
    Очищает текст от HTML тегов.

    Args:
        text: Исходный текст

    Returns:
        str: Очищенный текст
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
