"""
Обработчики callback_query (inline кнопок) Telegram бота.
Обрабатывает нажатия на кнопки в inline клавиатурах.
"""

import logging
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from bot.services.api_client import api_client
from bot.utils.keyboards import (
    get_main_menu_keyboard,
    get_task_keyboard,
    get_task_completed_keyboard,
    get_skip_keyboard
)
from bot.utils.messages import Messages

logger = logging.getLogger(__name__)


async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик кнопки "Главное меню".

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения
    """
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "📱 Главное меню\n\nВыберите действие:",
        reply_markup=get_main_menu_keyboard()
    )


async def handle_today_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик кнопки "Сегодняшнее задание".

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения
    """
    query = update.callback_query
    await query.answer()

    # Проверяем наличие токена
    token = context.user_data.get("token")

    if not token:
        await query.edit_message_text(Messages.ERROR_NO_TOKEN)
        return

    # Получаем задание на сегодня
    task = await api_client.get_today_task(token)

    if not task:
        await query.edit_message_text(
            Messages.NO_TASK_TODAY,
            reply_markup=get_main_menu_keyboard()
        )
        return

    # Проверяем статус задания
    if task.get("status") == "completed":
        await query.edit_message_text(
            Messages.TASK_ALREADY_COMPLETED,
            reply_markup=get_main_menu_keyboard()
        )
        return

    # Сохраняем задание в context для использования в "Подробнее"
    context.user_data["current_task"] = task

    # Форматируем и отправляем задание
    message = Messages.format_task(task)

    await query.edit_message_text(
        message,
        reply_markup=get_task_keyboard(task.get("id")),
        parse_mode="HTML"
    )


async def handle_my_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик кнопки "Мой прогресс".

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения
    """
    query = update.callback_query
    await query.answer()

    # Проверяем наличие токена
    token = context.user_data.get("token")

    if not token:
        await query.edit_message_text(Messages.ERROR_NO_TOKEN)
        return

    # Получаем статистику
    progress = await api_client.get_user_progress(token)

    if not progress:
        await query.edit_message_text(
            Messages.ERROR_GENERAL,
            reply_markup=get_main_menu_keyboard()
        )
        return

    # Форматируем и отправляем статистику
    message = Messages.format_progress(progress)

    await query.edit_message_text(
        message,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик кнопки "Помощь".

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения
    """
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        Messages.HELP_MESSAGE,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )


async def handle_complete_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик кнопки "Выполнить" для задания.
    Запускает процесс выполнения задания.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения
    """
    query = update.callback_query
    await query.answer()

    # Извлекаем task_id из callback_data
    task_id = query.data.replace("complete_task_", "")

    # Сохраняем ID задания
    context.user_data["current_task_id"] = task_id

    # Отправляем запрос на ответ с кнопкой "Пропустить"
    await query.message.reply_text(
        Messages.ASK_TASK_ANSWER,
        reply_markup=get_skip_keyboard()
    )

    # Помечаем что ожидаем ответ (для ConversationHandler)
    context.user_data["awaiting_task_answer"] = True


async def handle_task_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик кнопки "Подробнее" для задания.
    Показывает детальную информацию о задании.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения
    """
    query = update.callback_query
    await query.answer()

    # Извлекаем task_id из callback_data
    task_id = query.data.replace("task_details_", "")

    # Получаем задание из кеша (было сохранено в handle_today_task)
    task = context.user_data.get("current_task")

    if not task:
        await query.edit_message_text(
            Messages.ERROR_GENERAL,
            reply_markup=get_main_menu_keyboard()
        )
        return

    # Форматируем детальное описание
    message = Messages.format_task_details(task)

    await query.edit_message_text(
        message,
        reply_markup=get_task_keyboard(task_id),
        parse_mode="HTML"
    )


async def handle_skip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик кнопки "Пропустить".

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения
    """
    query = update.callback_query
    await query.answer()

    # Проверяем наличие токена
    token = context.user_data.get("token")
    task_id = context.user_data.get("current_task_id")

    if not token or not task_id:
        await query.edit_message_text(Messages.ERROR_GENERAL)
        return

    # Завершаем задание без ответа
    result = await api_client.complete_task(
        assignment_id=task_id,
        answer_text=None,
        token=token
    )

    if result:
        await query.edit_message_text(
            Messages.TASK_COMPLETED_SUCCESS,
            reply_markup=get_task_completed_keyboard()
        )

        logger.info(f"Task {task_id} completed (skipped) by user {update.effective_user.id}")

    else:
        await query.edit_message_text(
            Messages.ERROR_GENERAL,
            reply_markup=get_main_menu_keyboard()
        )

    # Очищаем данные
    context.user_data.pop("current_task_id", None)
    context.user_data.pop("awaiting_task_answer", None)


async def handle_task_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик текстовых сообщений когда ожидается ответ на задание.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения
    """
    # Проверяем, ожидаем ли мы ответ на задание
    if not context.user_data.get("awaiting_task_answer"):
        return

    # Проверяем наличие токена
    token = context.user_data.get("token")
    task_id = context.user_data.get("current_task_id")

    if not token or not task_id:
        await update.message.reply_text(Messages.ERROR_GENERAL)
        context.user_data.pop("awaiting_task_answer", None)
        return

    # Получаем ответ пользователя
    answer_text = update.message.text.strip()

    # Завершаем задание через API
    result = await api_client.complete_task(
        assignment_id=task_id,
        answer_text=answer_text if answer_text else None,
        token=token
    )

    if result:
        # Задание успешно выполнено
        # Получаем обновленную статистику
        progress = await api_client.get_user_progress(token)

        success_message = Messages.TASK_COMPLETED_SUCCESS

        if progress:
            success_message += f"\n\n{Messages.format_progress(progress)}"

        await update.message.reply_text(
            success_message,
            reply_markup=get_task_completed_keyboard(),
            parse_mode="HTML"
        )

        logger.info(f"Task {task_id} completed by user {update.effective_user.id}")

    else:
        # Ошибка при выполнении
        await update.message.reply_text(
            Messages.ERROR_GENERAL,
            reply_markup=get_main_menu_keyboard()
        )

    # Очищаем данные
    context.user_data.pop("current_task_id", None)
    context.user_data.pop("awaiting_task_answer", None)


# Создаем handlers для каждого типа callback
callback_handlers = [
    CallbackQueryHandler(handle_main_menu, pattern="^main_menu$"),
    CallbackQueryHandler(handle_today_task, pattern="^today_task$"),
    CallbackQueryHandler(handle_my_progress, pattern="^my_progress$"),
    CallbackQueryHandler(handle_help, pattern="^help$"),
    CallbackQueryHandler(handle_complete_task, pattern="^complete_task_"),
    CallbackQueryHandler(handle_task_details, pattern="^task_details_"),
    CallbackQueryHandler(handle_skip, pattern="^skip$"),
]
