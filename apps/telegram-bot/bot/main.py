"""
Главный модуль Telegram бота.
Точка входа для запуска бота.
"""

import logging
import html
import json
import traceback
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode
from bot.config import bot_settings
from bot.services.api_client import api_client

# Импорт handlers
from bot.handlers.start import registration_handler
from bot.handlers.commands import (
    help_handler,
    today_handler,
    progress_handler,
    cancel_handler
)
from bot.handlers.conversations import complete_task_handler
from bot.handlers.callbacks import callback_handlers, handle_task_answer

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, bot_settings.LOG_LEVEL)
)
logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик ошибок бота.
    Логирует все исключения и отправляет пользователю понятное сообщение.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения с информацией об ошибке
    """
    # Логируем ошибку
    logger.error("Exception while handling an update:", exc_info=context.error)

    # Формируем подробное сообщение об ошибке для логов
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    update_str = update.to_dict() if isinstance(update, Update) else str(update)

    error_message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    logger.error(error_message)

    # Отправляем пользователю дружелюбное сообщение
    if isinstance(update, Update) and update.effective_message:
        try:
            # Проверяем тип ошибки
            error_text = "😔 Произошла ошибка. Попробуйте позже."

            if context.error and hasattr(context.error, "response"):
                # Ошибка HTTP запроса
                status_code = getattr(context.error.response, "status_code", None)

                if status_code in [401, 403]:
                    error_text = (
                        "🔐 Ошибка авторизации.\n"
                        "Пожалуйста, зарегистрируйтесь заново: /start"
                    )

            await update.effective_message.reply_text(error_text)

        except Exception as e:
            logger.error(f"Error sending error message to user: {e}")


async def post_init(application: Application) -> None:
    """
    Callback после инициализации приложения.
    Проверяет доступность Backend API.

    Args:
        application: Объект Application
    """
    logger.info("Telegram bot initialized successfully")

    # Проверяем доступность Backend API
    api_available = await api_client.health_check()

    if api_available:
        logger.info("Backend API is available")
    else:
        logger.warning("Backend API is not available! Bot may not work correctly.")

    logger.info("Bot startup completed")


async def post_shutdown(application: Application) -> None:
    """
    Callback перед остановкой приложения.
    Закрывает соединения.

    Args:
        application: Объект Application
    """
    logger.info("Shutting down bot...")
    logger.info("Bot shutdown completed")


def main() -> None:
    """
    Главная функция запуска бота.
    Создает Application, регистрирует handlers и запускает бота.
    """
    logger.info("Starting Psychology Bot...")

    # Создаем Application
    application = (
        Application.builder()
        .token(bot_settings.TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )

    # Регистрация handlers (порядок важен!)

    # 1. ConversationHandlers (должны быть первыми)
    application.add_handler(registration_handler)
    application.add_handler(complete_task_handler)

    # 2. Обычные CommandHandlers
    application.add_handler(help_handler)
    application.add_handler(today_handler)
    application.add_handler(progress_handler)
    application.add_handler(cancel_handler)

    # 3. MessageHandler для ответов на задания
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task_answer)
    )

    # 4. CallbackQueryHandlers
    for callback_handler in callback_handlers:
        application.add_handler(callback_handler)

    # 5. Error handler (должен быть последним)
    application.add_error_handler(error_handler)

    # Запуск бота
    logger.info("Bot is running. Press Ctrl+C to stop.")
    logger.info(f"Registered {len(application.handlers[0])} handlers")

    application.run_polling(
        allowed_updates=["message", "callback_query"],
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
