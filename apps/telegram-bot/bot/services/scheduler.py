"""
Планировщик задач для отправки напоминаний и уведомлений.
Использует APScheduler для периодического выполнения задач.
"""

import logging
from datetime import datetime
from typing import TYPE_CHECKING
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.config import bot_settings
from bot.services.api_client import api_client

if TYPE_CHECKING:
    from telegram.ext import Application

logger = logging.getLogger(__name__)


class TaskScheduler:
    """
    Планировщик для автоматических задач бота.
    """

    def __init__(self, app: "Application"):
        """
        Инициализация планировщика.

        Args:
            app: Экземпляр Telegram Application
        """
        self.app = app
        self.scheduler = AsyncIOScheduler(
            timezone=bot_settings.SCHEDULER_TIMEZONE
        )

    async def send_morning_tasks(self):
        """
        Отправляет утренние задания всем пользователям.
        Запускается каждое утро в 09:00.
        """
        try:
            logger.info("Sending morning tasks...")

            if not bot_settings.ADMIN_TOKEN:
                logger.error("ADMIN_TOKEN not configured, skipping morning tasks")
                return

            # Получаем всех активных пользователей
            users = await api_client.get_all_users(bot_settings.ADMIN_TOKEN)

            if not users:
                logger.info("No users found or error getting users")
                return

            success_count = 0
            error_count = 0

            for user in users:
                try:
                    telegram_id = user.get("telegram_id")
                    if not telegram_id:
                        continue

                    # Получаем токен пользователя
                    user_data = await api_client.get_user_by_telegram_id(telegram_id)
                    if not user_data or "access_token" not in user_data:
                        logger.warning(f"Cannot get token for user {telegram_id}")
                        continue

                    token = user_data["access_token"]

                    # Получаем задание на сегодня
                    task = await api_client.get_today_task(token)

                    if not task:
                        logger.info(f"No task for user {telegram_id}")
                        continue

                    # Формируем сообщение
                    message = (
                        f"Доброе утро! {user.get('name', 'Пользователь')}\n\n"
                        f"📋 <b>Ваше задание на сегодня:</b>\n"
                        f"{task.get('title', 'Задание')}\n\n"
                        f"{task.get('description', '')}\n"
                    )

                    # Создаем inline клавиатуру
                    keyboard = [
                        [
                            InlineKeyboardButton(
                                "✅ Выполнить",
                                callback_data=f"complete_task_{task.get('id')}"
                            ),
                            InlineKeyboardButton(
                                "ℹ️ Подробнее",
                                callback_data=f"task_details_{task.get('id')}"
                            )
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)

                    # Отправляем сообщение
                    await self.app.bot.send_message(
                        chat_id=telegram_id,
                        text=message,
                        reply_markup=reply_markup,
                        parse_mode="HTML"
                    )

                    success_count += 1
                    logger.info(f"Morning task sent to user {telegram_id}")

                except Exception as e:
                    error_count += 1
                    logger.error(f"Error sending morning task to user: {str(e)}")

            logger.info(
                f"Morning tasks sent: {success_count} success, {error_count} errors"
            )

        except Exception as e:
            logger.error(f"Error in send_morning_tasks: {str(e)}")

    async def send_evening_reminder(self):
        """
        Отправляет вечернее напоминание тем, кто не выполнил задание.
        Запускается в 20:00.
        """
        try:
            logger.info("Sending evening reminders...")

            if not bot_settings.ADMIN_TOKEN:
                logger.error("ADMIN_TOKEN not configured, skipping evening reminders")
                return

            # Получаем всех пользователей
            users = await api_client.get_all_users(bot_settings.ADMIN_TOKEN)

            if not users:
                logger.info("No users found")
                return

            success_count = 0
            error_count = 0

            for user in users:
                try:
                    telegram_id = user.get("telegram_id")
                    if not telegram_id:
                        continue

                    # Получаем токен пользователя
                    user_data = await api_client.get_user_by_telegram_id(telegram_id)
                    if not user_data or "access_token" not in user_data:
                        continue

                    token = user_data["access_token"]

                    # Получаем задание на сегодня
                    task = await api_client.get_today_task(token)

                    # Проверяем, не выполнено ли задание
                    if task and task.get("status") != "completed":
                        message = (
                            f"🔔 <b>Напоминание</b>\n\n"
                            f"У вас ещё есть время выполнить сегодняшнее задание:\n"
                            f"📋 {task.get('title', 'Задание')}\n\n"
                            f"Не упустите возможность продолжить свой прогресс!"
                        )

                        keyboard = [
                            [
                                InlineKeyboardButton(
                                    "✅ Выполнить сейчас",
                                    callback_data=f"complete_task_{task.get('id')}"
                                )
                            ]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)

                        await self.app.bot.send_message(
                            chat_id=telegram_id,
                            text=message,
                            reply_markup=reply_markup,
                            parse_mode="HTML"
                        )

                        success_count += 1
                        logger.info(f"Evening reminder sent to user {telegram_id}")

                except Exception as e:
                    error_count += 1
                    logger.error(f"Error sending evening reminder: {str(e)}")

            logger.info(
                f"Evening reminders sent: {success_count} success, {error_count} errors"
            )

        except Exception as e:
            logger.error(f"Error in send_evening_reminder: {str(e)}")

    def start(self):
        """
        Запускает планировщик и регистрирует задачи.
        """
        logger.info("Starting task scheduler...")

        # Парсим время из конфига
        morning_hour, morning_minute = map(int, bot_settings.MORNING_TASK_TIME.split(":"))
        evening_hour, evening_minute = map(int, bot_settings.EVENING_REMINDER_TIME.split(":"))

        # Утренние задания
        self.scheduler.add_job(
            self.send_morning_tasks,
            trigger=CronTrigger(
                hour=morning_hour,
                minute=morning_minute,
                timezone=bot_settings.SCHEDULER_TIMEZONE
            ),
            id="morning_tasks",
            name="Send morning tasks",
            replace_existing=True
        )

        # Вечерние напоминания
        self.scheduler.add_job(
            self.send_evening_reminder,
            trigger=CronTrigger(
                hour=evening_hour,
                minute=evening_minute,
                timezone=bot_settings.SCHEDULER_TIMEZONE
            ),
            id="evening_reminders",
            name="Send evening reminders",
            replace_existing=True
        )

        self.scheduler.start()
        logger.info(
            f"Task scheduler started successfully. "
            f"Morning tasks: {bot_settings.MORNING_TASK_TIME}, "
            f"Evening reminders: {bot_settings.EVENING_REMINDER_TIME}"
        )

    def stop(self):
        """
        Останавливает планировщик.
        """
        logger.info("Stopping task scheduler...")
        self.scheduler.shutdown()
        logger.info("Task scheduler stopped")

    def get_scheduled_jobs(self):
        """
        Возвращает список всех запланированных задач.

        Returns:
            list: Список задач в планировщике
        """
        return self.scheduler.get_jobs()
