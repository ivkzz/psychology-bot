"""
Модуль с текстовыми сообщениями Telegram бота.
Все сообщения сгруппированы в одном месте для удобства перевода и изменения.
"""

from typing import Dict, Any, Optional


class Messages:
    """Класс с текстовыми сообщениями бота."""

    # Приветствия и стартовые сообщения
    WELCOME_NEW_USER = (
        "👋 Добро пожаловать в Психолог-бот!\n\n"
        "Я помогу вам развивать эмоциональный интеллект и поддерживать "
        "психологическое здоровье через регулярные практики.\n\n"
        "Для начала работы мне нужно задать вам несколько вопросов."
    )

    WELCOME_EXISTING_USER = (
        "С возвращением! 👋\n\n"
        "Рад снова видеть вас. Готовы продолжить работу над собой?"
    )

    # Регистрация
    ASK_NAME = "Как я могу к вам обращаться? Введите ваше имя:"
    ASK_EMAIL = "Отлично, {name}! Теперь введите ваш email для доступа к веб-версии:"
    ASK_PASSWORD = (
        "Придумайте пароль для доступа к веб-версии.\n"
        "Пароль должен содержать минимум 8 символов:"
    )
    REGISTRATION_SUCCESS = (
        "🎉 Регистрация успешно завершена!\n\n"
        "Теперь вы можете использовать бот и веб-версию.\n"
        "Email: {email}\n\n"
        "Давайте начнем! Выберите действие:"
    )
    REGISTRATION_ERROR = (
        "😔 Произошла ошибка при регистрации.\n"
        "Возможно, этот email уже используется.\n\n"
        "Попробуйте снова: /start"
    )

    # Команды
    HELP_MESSAGE = (
        "📚 <b>Доступные команды:</b>\n\n"
        "/start - Начать работу с ботом\n"
        "/today - Получить задание на сегодня\n"
        "/done - Отметить задание как выполненное\n"
        "/progress - Посмотреть свой прогресс\n"
        "/help - Показать эту справку\n"
        "/cancel - Отменить текущее действие\n\n"
        "💡 Также вы можете использовать кнопки меню для навигации."
    )

    NO_TASK_TODAY = (
        "😊 На сегодня у вас нет активных заданий.\n"
        "Отдохните или вернитесь завтра!"
    )

    TASK_ALREADY_COMPLETED = (
        "✅ Это задание уже выполнено!\n"
        "Отличная работа! Ждите новое задание завтра."
    )

    ASK_TASK_ANSWER = (
        "📝 Поделитесь своими ощущениями от упражнения.\n\n"
        "Что вы почувствовали? Какие мысли возникли?\n"
        "(Или отправьте /skip чтобы пропустить)"
    )

    TASK_COMPLETED_SUCCESS = (
        "🎉 Отлично! Задание выполнено!\n\n"
        "Вы делаете успехи в развитии эмоционального интеллекта.\n"
        "Продолжайте в том же духе!"
    )

    TASK_SKIPPED = (
        "Задание пропущено. Вы можете выполнить его позже."
    )

    # Ошибки
    ERROR_GENERAL = (
        "😔 Произошла ошибка. Попробуйте позже или обратитесь в поддержку."
    )

    ERROR_AUTH = (
        "🔐 Ошибка авторизации.\n"
        "Пожалуйста, зарегистрируйтесь заново: /start"
    )

    ERROR_NO_TOKEN = (
        "Вы не авторизованы. Используйте /start для регистрации."
    )

    # Отмена
    CANCELLED = "Действие отменено. Чем могу помочь?"
    NOTHING_TO_CANCEL = "Нет активных действий для отмены."

    # Прогресс
    @staticmethod
    def format_progress(progress: Dict[str, Any]) -> str:
        """
        Форматирует данные о прогрессе пользователя.

        Args:
            progress: Словарь с данными о прогрессе

        Returns:
            Отформатированное сообщение с прогрессом
        """
        total_tasks = progress.get("total_tasks", 0)
        completed_tasks = progress.get("completed_tasks", 0)
        current_streak = progress.get("current_streak", 0)
        longest_streak = progress.get("longest_streak", 0)

        completion_rate = 0
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100

        message = (
            f"📊 <b>Ваша статистика</b>\n\n"
            f"✅ Выполнено заданий: {completed_tasks} из {total_tasks}\n"
            f"📈 Процент выполнения: {completion_rate:.1f}%\n"
            f"🔥 Текущая серия: {current_streak} дней\n"
            f"🏆 Рекорд серии: {longest_streak} дней\n\n"
        )

        if current_streak >= 7:
            message += "🌟 Отличная работа! Вы держите стабильную серию!"
        elif current_streak >= 3:
            message += "💪 Хорошая работа! Продолжайте в том же духе!"
        else:
            message += "📅 Выполняйте задания каждый день для серии!"

        return message

    @staticmethod
    def format_task(assignment: Dict[str, Any]) -> str:
        """
        Форматирует информацию о задании.

        Args:
            assignment: Словарь с данными о назначении (может содержать вложенный task)

        Returns:
            Отформатированное сообщение с заданием
        """
        # Проверяем, это Assignment или сам Task
        task = assignment.get("task", assignment)

        title = task.get("title", "Задание")
        description = task.get("description", "")
        category = task.get("category", "")
        difficulty = task.get("difficulty", "")

        message = f"📋 <b>{title}</b>\n\n"

        if category:
            message += f"🏷 Категория: {category}\n"

        if difficulty:
            difficulty_emoji = {
                "easy": "🟢",
                "medium": "🟡",
                "hard": "🔴"
            }.get(difficulty.lower(), "⚪️")
            message += f"{difficulty_emoji} Сложность: {difficulty}\n"

        message += f"\n{description}\n"

        return message

    @staticmethod
    def format_task_details(assignment: Dict[str, Any]) -> str:
        """
        Форматирует детальную информацию о задании.

        Args:
            assignment: Словарь с данными о назначении (может содержать вложенный task)

        Returns:
            Отформатированное детальное сообщение
        """
        base_info = Messages.format_task(assignment)

        # Проверяем, это Assignment или сам Task
        task = assignment.get("task", assignment)

        instructions = task.get("instructions", "")
        expected_time = task.get("expected_time", "")
        tips = task.get("tips", "")

        message = base_info

        if instructions:
            message += f"\n📖 <b>Инструкция:</b>\n{instructions}\n"

        if expected_time:
            message += f"\n⏱ Время выполнения: {expected_time} минут\n"

        if tips:
            message += f"\n💡 <b>Подсказка:</b>\n{tips}\n"

        return message
