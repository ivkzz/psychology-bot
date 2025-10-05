"""
Модуль для создания inline клавиатур Telegram бота.
Все клавиатуры сгруппированы в одном месте для удобства поддержки.
"""

from typing import Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Главное меню бота.

    Returns:
        InlineKeyboardMarkup с основными кнопками меню
    """
    keyboard = [
        [
            InlineKeyboardButton("📋 Сегодняшнее задание", callback_data="today_task")
        ],
        [
            InlineKeyboardButton("📈 Мой прогресс", callback_data="my_progress")
        ],
        [
            InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_task_keyboard(task_id: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для задания.

    Args:
        task_id: ID задания

    Returns:
        InlineKeyboardMarkup с кнопками для задания
    """
    keyboard = [
        [
            InlineKeyboardButton("✅ Выполнить", callback_data=f"complete_task_{task_id}"),
            InlineKeyboardButton("📝 Подробнее", callback_data=f"task_details_{task_id}")
        ],
        [
            InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_task_completed_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура после выполнения задания.

    Returns:
        InlineKeyboardMarkup с кнопками после выполнения
    """
    keyboard = [
        [
            InlineKeyboardButton("📊 Посмотреть статистику", callback_data="my_progress")
        ],
        [
            InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_skip_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой пропустить.

    Returns:
        InlineKeyboardMarkup с кнопкой пропустить
    """
    keyboard = [
        [
            InlineKeyboardButton("⏭️ Пропустить", callback_data="skip")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_confirmation_keyboard(action: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для подтверждения действия.

    Args:
        action: Действие для подтверждения

    Returns:
        InlineKeyboardMarkup с кнопками подтверждения
    """
    keyboard = [
        [
            InlineKeyboardButton("✅ Да", callback_data=f"confirm_{action}"),
            InlineKeyboardButton("❌ Нет", callback_data=f"cancel_{action}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Простая клавиатура с кнопкой возврата в меню.

    Returns:
        InlineKeyboardMarkup с кнопкой возврата
    """
    keyboard = [
        [
            InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
