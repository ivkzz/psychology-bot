"""
Telegram Sender Service.
Отправка сообщений через Telegram Bot API.
"""

import logging
from typing import Optional
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


class TelegramSender:
    """Сервис для отправки сообщений через Telegram Bot API."""

    def __init__(self):
        """Инициализация сервиса."""
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    async def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: str = "HTML",
        reply_markup: Optional[dict] = None
    ) -> bool:
        """
        Отправить сообщение пользователю.

        Args:
            chat_id: ID чата в Telegram
            text: Текст сообщения
            parse_mode: Режим парсинга (HTML/Markdown)
            reply_markup: Inline клавиатура

        Returns:
            bool: True если успешно отправлено
        """
        try:
            url = f"{self.base_url}/sendMessage"

            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode
            }

            if reply_markup:
                payload["reply_markup"] = reply_markup

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

            logger.info(f"Message sent to chat_id={chat_id}")
            return True

        except Exception as e:
            logger.error(f"Error sending message to chat_id={chat_id}: {str(e)}")
            return False

    def format_morning_message(self, user_name: str, task: dict) -> str:
        """
        Форматирует утреннее сообщение с заданием.

        Args:
            user_name: Имя пользователя
            task: Данные задания

        Returns:
            str: Отформатированное сообщение
        """
        return (
            f"☀️ Доброе утро, {user_name}!\n\n"
            f"📋 <b>Ваше задание на сегодня:</b>\n"
            f"{task.get('title', 'Задание')}\n\n"
            f"📝 <b>Описание:</b>\n"
            f"{task.get('description', '')}\n\n"
            f"Используйте команду /today чтобы посмотреть задание и выполнить его."
        )

    def format_evening_reminder(self, task: dict) -> str:
        """
        Форматирует вечернее напоминание.

        Args:
            task: Данные задания

        Returns:
            str: Отформатированное сообщение
        """
        return (
            f"🔔 <b>Напоминание</b>\n\n"
            f"У вас ещё есть время выполнить сегодняшнее задание:\n"
            f"📋 {task.get('title', 'Задание')}\n\n"
            f"Не упустите возможность продолжить свой прогресс!\n\n"
            f"Используйте команду /today для выполнения задания."
        )


# Создаем глобальный экземпляр
telegram_sender = TelegramSender()
