"""
Общие константы, используемые во всех частях проекта.
"""

from enum import Enum


class UserRole(str, Enum):
    """Роли пользователей в системе."""
    USER = "user"
    ADMIN = "admin"


class TaskStatus(str, Enum):
    """Статусы заданий."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Приоритеты заданий."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class NotificationType(str, Enum):
    """Типы уведомлений."""
    TASK_ASSIGNED = "task_assigned"
    TASK_REMINDER = "task_reminder"
    TASK_DEADLINE = "task_deadline"
    SYSTEM = "system"


# Ограничения и лимиты
MAX_TASK_TITLE_LENGTH = 200
MAX_TASK_DESCRIPTION_LENGTH = 2000
MAX_USERNAME_LENGTH = 50
MAX_EMAIL_LENGTH = 100

# Временные константы
DEFAULT_TASK_DURATION_DAYS = 7
REMINDER_BEFORE_DEADLINE_HOURS = 24

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
