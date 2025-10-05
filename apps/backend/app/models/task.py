"""
Модель задания (шаблона упражнения) для системы психолог-бота.
"""

from datetime import datetime
import uuid
import enum
from sqlalchemy import Column, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class TaskDifficulty(str, enum.Enum):
    """Уровни сложности заданий."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Task(Base):
    """
    Модель шаблона задания для психологических упражнений.

    Attributes:
        id: Уникальный идентификатор задания (UUID)
        title: Название задания
        description: Подробное описание упражнения
        category: Категория упражнения (медитация, дыхание, благодарности и т.д.)
        difficulty: Уровень сложности (easy/medium/hard)
        created_at: Дата и время создания
        assignments: Связь с назначениями этого задания пользователям
    """

    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    difficulty = Column(SQLEnum(TaskDifficulty), nullable=False, default=TaskDifficulty.MEDIUM)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    assignments = relationship("Assignment", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title={self.title}, category={self.category}, difficulty={self.difficulty})>"
