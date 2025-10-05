"""
Обработчики основных команд Telegram бота.
Включает команды: /help, /today, /done, /progress, /cancel
"""

import logging
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.services.api_client import api_client
from bot.utils.keyboards import get_task_keyboard, get_main_menu_keyboard
from bot.utils.messages import Messages

logger = logging.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /help.
    Отображает список доступных команд.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения
    """
    await update.message.reply_text(
        Messages.HELP_MESSAGE,
        parse_mode="HTML"
    )


async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /today.
    Отображает задание на сегодня.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения
    """
    # Проверяем наличие токена
    token = context.user_data.get("token")

    if not token:
        await update.message.reply_text(Messages.ERROR_NO_TOKEN)
        return

    # Получаем задание на сегодня
    task = await api_client.get_today_task(token)

    if not task:
        await update.message.reply_text(
            Messages.NO_TASK_TODAY,
            reply_markup=get_main_menu_keyboard()
        )
        return

    # Проверяем статус задания
    if task.get("status") == "completed":
        await update.message.reply_text(Messages.TASK_ALREADY_COMPLETED)
        return

    # Форматируем и отправляем задание
    message = Messages.format_task(task)

    await update.message.reply_text(
        message,
        reply_markup=get_task_keyboard(task.get("id")),
        parse_mode="HTML"
    )


async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /done.
    Инициирует процесс завершения задания.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения
    """
    # Проверяем наличие токена
    token = context.user_data.get("token")

    if not token:
        await update.message.reply_text(Messages.ERROR_NO_TOKEN)
        return

    # Получаем задание на сегодня
    task = await api_client.get_today_task(token)

    if not task:
        await update.message.reply_text(Messages.NO_TASK_TODAY)
        return

    # Проверяем статус задания
    if task.get("status") == "completed":
        await update.message.reply_text(Messages.TASK_ALREADY_COMPLETED)
        return

    # Сохраняем ID задания для использования в ConversationHandler
    context.user_data["current_task_id"] = task.get("id")

    # Запрашиваем ответ пользователя
    await update.message.reply_text(Messages.ASK_TASK_ANSWER)


async def progress_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /progress.
    Отображает статистику прогресса пользователя.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения
    """
    # Проверяем наличие токена
    token = context.user_data.get("token")

    if not token:
        await update.message.reply_text(Messages.ERROR_NO_TOKEN)
        return

    # Получаем статистику
    progress = await api_client.get_user_progress(token)

    if not progress:
        await update.message.reply_text(
            Messages.ERROR_GENERAL,
            reply_markup=get_main_menu_keyboard()
        )
        return

    # Форматируем и отправляем статистику
    message = Messages.format_progress(progress)

    await update.message.reply_text(
        message,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /cancel.
    Отменяет текущую операцию.

    Args:
        update: Объект Update от Telegram
        context: Контekст выполнения
    """
    # Очищаем текущий контекст
    context.user_data.pop("current_task_id", None)
    context.user_data.pop("awaiting_task_answer", None)

    await update.message.reply_text(
        Messages.CANCELLED,
        reply_markup=get_main_menu_keyboard()
    )


# Создаем handlers для каждой команды
help_handler = CommandHandler("help", help_command)
today_handler = CommandHandler("today", today_command)
done_handler = CommandHandler("done", done_command)
progress_handler = CommandHandler("progress", progress_command)
cancel_handler = CommandHandler("cancel", cancel_command)
