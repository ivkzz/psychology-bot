"""
Task Scheduler Service.
Планировщик для автоматической отправки заданий и напоминаний.
"""

import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.crud import user as user_crud, assignment as assignment_crud, task as task_crud
from app.services.telegram_sender import telegram_sender

logger = logging.getLogger(__name__)


class TaskScheduler:
    """Планировщик задач для отправки заданий и напоминаний."""

    def __init__(self):
        """Инициализация планировщика."""
        self.scheduler = AsyncIOScheduler(
            timezone=settings.SCHEDULER_TIMEZONE
        )

    async def send_morning_tasks(self):
        """
        Отправляет утренние задания всем активным пользователям.
        Запускается каждое утро в заданное время.
        """
        try:
            import sys
            print("🌅 Starting morning tasks distribution...", flush=True)
            sys.stdout.flush()
            logger.info("Starting morning tasks distribution...")

            async with AsyncSessionLocal() as db:
                # Получаем всех активных пользователей
                users = await user_crud.get_all(db, is_active=True)

                if not users:
                    logger.info("No active users found")
                    return

                success_count = 0
                error_count = 0

                for user in users:
                    try:
                        # Пропускаем пользователей без Telegram ID
                        if not user.telegram_id:
                            print(f"⏭️  Skipping {user.name} - no telegram_id", flush=True)
                            sys.stdout.flush()
                            continue

                        # Получаем задание на сегодня для пользователя
                        assignment = await assignment_crud.get_today_assignment(
                            db, user.id
                        )

                        # Если задание уже выполнено - пропускаем отправку (не отправляем повторно)
                        if assignment and assignment.status.value == "completed":
                            print(f"⏭️  {user.name} already completed today's task", flush=True)
                            sys.stdout.flush()
                            continue

                        # Если нет задания - создаем новое
                        if not assignment:
                            print(f"📝 No assignment for {user.name}, creating new...", flush=True)
                            sys.stdout.flush()

                            # Выбираем случайную задачу
                            random_task = await task_crud.get_random_task(db)

                            if not random_task:
                                logger.error(f"No tasks available in database for user {user.id}")
                                print(f"❌ No tasks in database!", flush=True)
                                sys.stdout.flush()
                                error_count += 1
                                continue

                            # Создаем назначение
                            assignment = await assignment_crud.create_daily_assignment(
                                db, user.id, random_task.id
                            )
                            print(f"✅ Created assignment: {assignment.task.title}", flush=True)
                            sys.stdout.flush()

                        # Формируем сообщение
                        task_data = {
                            "title": assignment.task.title,
                            "description": assignment.task.description
                        }
                        message = telegram_sender.format_morning_message(
                            user.name, task_data
                        )

                        # Отправляем сообщение
                        print(f"📤 Sending morning task to {user.name} (telegram_id: {user.telegram_id})", flush=True)
                        print(f"   Task: {assignment.task.title}", flush=True)
                        sys.stdout.flush()
                        sent = await telegram_sender.send_message(
                            chat_id=user.telegram_id,
                            text=message
                        )

                        if sent:
                            success_count += 1
                            print(f"✅ Morning task sent to user {user.id}", flush=True)
                            sys.stdout.flush()
                            logger.info(f"Morning task sent to user {user.id}")
                        else:
                            error_count += 1
                            print(f"❌ Failed to send to user {user.id}", flush=True)
                            sys.stdout.flush()

                    except Exception as e:
                        error_count += 1
                        print(f"❌ Exception for user {user.id}: {str(e)}", flush=True)
                        sys.stdout.flush()
                        logger.error(f"Error sending morning task to user {user.id}: {str(e)}")

                logger.info(
                    f"Morning tasks distribution completed: "
                    f"{success_count} success, {error_count} errors"
                )

        except Exception as e:
            logger.error(f"Error in send_morning_tasks: {str(e)}")

    async def send_evening_reminders(self):
        """
        Отправляет вечерние напоминания пользователям с невыполненными заданиями.
        Запускается каждый вечер в заданное время.
        """
        try:
            logger.info("Starting evening reminders...")

            async with AsyncSessionLocal() as db:
                # Получаем всех активных пользователей
                users = await user_crud.get_all(db, is_active=True)

                if not users:
                    logger.info("No active users found")
                    return

                success_count = 0
                error_count = 0

                for user in users:
                    try:
                        # Пропускаем пользователей без Telegram ID
                        if not user.telegram_id:
                            continue

                        # Получаем задание на сегодня
                        assignment = await assignment_crud.get_today_assignment(
                            db, user.id
                        )

                        if not assignment:
                            continue

                        # Отправляем напоминание только если задание НЕ выполнено
                        if assignment.status.value != "completed":
                            task_data = {
                                "title": assignment.task.title
                            }
                            message = telegram_sender.format_evening_reminder(task_data)

                            # Отправляем сообщение
                            sent = await telegram_sender.send_message(
                                chat_id=user.telegram_id,
                                text=message
                            )

                            if sent:
                                success_count += 1
                                logger.info(f"Evening reminder sent to user {user.id}")
                            else:
                                error_count += 1

                    except Exception as e:
                        error_count += 1
                        logger.error(f"Error sending evening reminder to user {user.id}: {str(e)}")

                logger.info(
                    f"Evening reminders completed: "
                    f"{success_count} success, {error_count} errors"
                )

        except Exception as e:
            logger.error(f"Error in send_evening_reminders: {str(e)}")

    def start(self):
        """Запускает планировщик и регистрирует задачи."""
        import sys
        print("📋 TaskScheduler.start() called", flush=True)
        sys.stdout.flush()
        logger.info("Starting task scheduler...")

        # Парсим время из конфига
        morning_hour, morning_minute = map(
            int, settings.MORNING_TASK_TIME.split(":")
        )
        evening_hour, evening_minute = map(
            int, settings.EVENING_REMINDER_TIME.split(":")
        )

        print(f"📋 Adding morning job: {morning_hour}:{morning_minute}", flush=True)
        sys.stdout.flush()
        # Утренние задания
        self.scheduler.add_job(
            self.send_morning_tasks,
            trigger=CronTrigger(
                hour=morning_hour,
                minute=morning_minute,
                timezone=settings.SCHEDULER_TIMEZONE
            ),
            id="morning_tasks",
            name="Send morning tasks",
            replace_existing=True
        )

        print(f"📋 Adding evening job: {evening_hour}:{evening_minute}", flush=True)
        sys.stdout.flush()
        # Вечерние напоминания
        self.scheduler.add_job(
            self.send_evening_reminders,
            trigger=CronTrigger(
                hour=evening_hour,
                minute=evening_minute,
                timezone=settings.SCHEDULER_TIMEZONE
            ),
            id="evening_reminders",
            name="Send evening reminders",
            replace_existing=True
        )

        print("📋 Starting scheduler...", flush=True)
        sys.stdout.flush()
        self.scheduler.start()

        jobs = self.scheduler.get_jobs()
        print(f"📋 Scheduler started with {len(jobs)} jobs", flush=True)
        for job in jobs:
            print(f"   - {job.id}: next run at {job.next_run_time}", flush=True)
        sys.stdout.flush()

        logger.info(
            f"Task scheduler started successfully. "
            f"Morning tasks: {settings.MORNING_TASK_TIME}, "
            f"Evening reminders: {settings.EVENING_REMINDER_TIME}"
        )

    def stop(self):
        """Останавливает планировщик."""
        logger.info("Stopping task scheduler...")
        self.scheduler.shutdown()
        logger.info("Task scheduler stopped")


# Создаем глобальный экземпляр
task_scheduler = TaskScheduler()
