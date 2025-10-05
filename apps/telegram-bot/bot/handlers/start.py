"""
Обработчик команды /start для Telegram бота.
Включает ConversationHandler для регистрации новых пользователей.
"""

import logging
from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
from bot.services.api_client import api_client
from bot.utils.keyboards import get_main_menu_keyboard
from bot.utils.messages import Messages

logger = logging.getLogger(__name__)

# Состояния диалога регистрации
ASK_NAME, ASK_EMAIL, ASK_PASSWORD = range(3)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик команды /start.
    Проверяет зарегистрирован ли пользователь, если нет - запускает регистрацию.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения

    Returns:
        Следующее состояние диалога или ConversationHandler.END
    """
    user = update.effective_user
    telegram_id = user.id

    # Проверяем, зарегистрирован ли пользователь
    user_data = await api_client.get_user_by_telegram_id(telegram_id)

    if user_data and "access_token" in user_data:
        # Пользователь уже зарегистрирован
        context.user_data["token"] = user_data["access_token"]
        context.user_data["user_info"] = user_data

        await update.message.reply_text(
            Messages.WELCOME_EXISTING_USER,
            reply_markup=get_main_menu_keyboard()
        )
        return ConversationHandler.END

    # Новый пользователь - начинаем регистрацию
    await update.message.reply_text(Messages.WELCOME_NEW_USER)
    await update.message.reply_text(Messages.ASK_NAME)

    return ASK_NAME


async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Получает имя пользователя и запрашивает email.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения

    Returns:
        Следующее состояние ASK_EMAIL
    """
    name = update.message.text.strip()

    if not name or len(name) < 2:
        await update.message.reply_text(
            "Пожалуйста, введите корректное имя (минимум 2 символа):"
        )
        return ASK_NAME

    context.user_data["registration_name"] = name

    await update.message.reply_text(
        Messages.ASK_EMAIL.format(name=name)
    )

    return ASK_EMAIL


async def receive_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Получает email пользователя и запрашивает пароль.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения

    Returns:
        Следующее состояние ASK_PASSWORD
    """
    email = update.message.text.strip().lower()

    # Простая валидация email
    if "@" not in email or "." not in email.split("@")[-1]:
        await update.message.reply_text(
            "Пожалуйста, введите корректный email адрес:"
        )
        return ASK_EMAIL

    context.user_data["registration_email"] = email

    await update.message.reply_text(Messages.ASK_PASSWORD)

    return ASK_PASSWORD


async def receive_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Получает пароль и завершает регистрацию пользователя.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения

    Returns:
        ConversationHandler.END
    """
    password = update.message.text.strip()

    # Валидация пароля
    if len(password) < 8:
        await update.message.reply_text(
            "Пароль слишком короткий. Минимум 8 символов.\n"
            "Попробуйте снова:"
        )
        return ASK_PASSWORD

    # Удаляем сообщение с паролем для безопасности
    try:
        await update.message.delete()
    except Exception:
        pass

    user = update.effective_user
    name = context.user_data.get("registration_name")
    email = context.user_data.get("registration_email")

    # Регистрируем пользователя через API
    result = await api_client.register_user(
        name=name,
        email=email,
        password=password,
        telegram_id=user.id
    )

    if result and "access_token" in result:
        # Регистрация успешна
        context.user_data["token"] = result["access_token"]
        context.user_data["user_info"] = result.get("user", {})

        # Очищаем временные данные регистрации
        context.user_data.pop("registration_name", None)
        context.user_data.pop("registration_email", None)

        await update.message.reply_text(
            Messages.REGISTRATION_SUCCESS.format(email=email),
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )

        logger.info(f"User {user.id} registered successfully")

    else:
        # Ошибка регистрации
        await update.message.reply_text(Messages.REGISTRATION_ERROR)

        # Очищаем данные
        context.user_data.pop("registration_name", None)
        context.user_data.pop("registration_email", None)

        logger.error(f"Failed to register user {user.id}")

    return ConversationHandler.END


async def cancel_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Отменяет процесс регистрации.

    Args:
        update: Объект Update от Telegram
        context: Контекст выполнения

    Returns:
        ConversationHandler.END
    """
    # Очищаем данные регистрации
    context.user_data.pop("registration_name", None)
    context.user_data.pop("registration_email", None)

    await update.message.reply_text(
        "Регистрация отменена.\n"
        "Для повторной попытки используйте /start"
    )

    return ConversationHandler.END


# Создаем ConversationHandler для регистрации
registration_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_command)],
    states={
        ASK_NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)
        ],
        ASK_EMAIL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_email)
        ],
        ASK_PASSWORD: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, receive_password)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel_registration)],
    name="registration",
    persistent=False
)
