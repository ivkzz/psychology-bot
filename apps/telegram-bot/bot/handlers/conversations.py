"""
ConversationHandler для многошаговых диалогов Telegram бота.
Включает диалог для выполнения заданий с получением ответа от пользователя.
"""

import logging
from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from bot.services.api_client import api_client
from bot.utils.keyboards import get_task_completed_keyboard, get_main_menu_keyboard
from bot.utils.messages import Messages

logger = logging.getLogger(__name__)

# Состояния диалога выполнения задания
AWAITING_ANSWER = 0


async def start_complete_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Начало процесса выполнения задания.
    Вызывается после команды /done.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения

    Returns:
        Состояние AWAITING_ANSWER
    """
    # Проверяем наличие токена
    token = context.user_data.get("token")

    if not token:
        await update.message.reply_text(Messages.ERROR_NO_TOKEN)
        return ConversationHandler.END

    # Получаем задание на сегодня
    task = await api_client.get_today_task(token)

    if not task:
        await update.message.reply_text(Messages.NO_TASK_TODAY)
        return ConversationHandler.END

    # Проверяем статус задания
    if task.get("status") == "completed":
        await update.message.reply_text(Messages.TASK_ALREADY_COMPLETED)
        return ConversationHandler.END

    # Сохраняем ID задания
    context.user_data["current_task_id"] = task.get("id")

    # Запрашиваем ответ пользователя
    await update.message.reply_text(Messages.ASK_TASK_ANSWER)

    return AWAITING_ANSWER


async def receive_task_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Получает ответ пользователя и завершает задание.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения

    Returns:
        ConversationHandler.END
    """
    # Проверяем наличие токена
    token = context.user_data.get("token")
    task_id = context.user_data.get("current_task_id")

    if not token or not task_id:
        await update.message.reply_text(Messages.ERROR_GENERAL)
        return ConversationHandler.END

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

    return ConversationHandler.END


async def skip_task_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Пропускает ввод ответа и завершает задание без комментария.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения

    Returns:
        ConversationHandler.END
    """
    # Проверяем наличие токена
    token = context.user_data.get("token")
    task_id = context.user_data.get("current_task_id")

    if not token or not task_id:
        await update.message.reply_text(Messages.ERROR_GENERAL)
        return ConversationHandler.END

    # Завершаем задание без ответа
    result = await api_client.complete_task(
        assignment_id=task_id,
        answer_text=None,
        token=token
    )

    if result:
        await update.message.reply_text(
            Messages.TASK_COMPLETED_SUCCESS,
            reply_markup=get_task_completed_keyboard()
        )

        logger.info(f"Task {task_id} completed (skipped answer) by user {update.effective_user.id}")

    else:
        await update.message.reply_text(
            Messages.ERROR_GENERAL,
            reply_markup=get_main_menu_keyboard()
        )

    # Очищаем данные
    context.user_data.pop("current_task_id", None)

    return ConversationHandler.END


async def cancel_complete_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Отменяет процесс выполнения задания.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения

    Returns:
        ConversationHandler.END
    """
    # Очищаем данные
    context.user_data.pop("current_task_id", None)

    await update.message.reply_text(
        Messages.CANCELLED,
        reply_markup=get_main_menu_keyboard()
    )

    return ConversationHandler.END


# Создаем ConversationHandler для выполнения задания
complete_task_handler = ConversationHandler(
    entry_points=[
        CommandHandler("done", start_complete_task)
    ],
    states={
        AWAITING_ANSWER: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & ~filters.Regex(r"^/skip$"),
                receive_task_answer
            ),
            CommandHandler("skip", skip_task_answer)
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel_complete_task)
    ],
    name="complete_task",
    persistent=False
)
