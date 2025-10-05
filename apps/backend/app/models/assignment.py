"""
Модель назначения задания пользователю.
"""

from datetime import datetime, date
import uuid
import enum
from sqlalchemy import Column, String, Text, DateTime, Date, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class AssignmentStatus(str, enum.Enum):
    """Статусы выполнения задания."""
    PENDING = "pending"
    COMPLETED = "completed"


class Assignment(Base):
    """
    Модель назначения задания конкретному пользователю.

    Attributes:
        id: Уникальный идентификатор назначения (UUID)
        user_id: ID пользователя (FK к User)
        task_id: ID задания (FK к Task)
        assigned_date: Дата назначения задания
        completed_at: Дата и время выполнения (опционально)
        status: Статус выполнения (pending/completed)
        answer_text: Текстовый ответ пользователя на задание (опционально)
        created_at: Дата и время создания записи
        user: Связь с пользователем
        task: Связь с заданием
    """

    __tablename__ = "assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    assigned_date = Column(Date, nullable=False, default=date.today, index=True)
    completed_at = Column(DateTime, nullable=True)
    status = Column(SQLEnum(AssignmentStatus), nullable=False, default=AssignmentStatus.PENDING, index=True)
    answer_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="assignments")
    task = relationship("Task", back_populates="assignments")

    # Composite indexes для оптимизации запросов
    __table_args__ = (
        Index('ix_assignments_user_date', 'user_id', 'assigned_date'),
        Index('ix_assignments_user_status', 'user_id', 'status'),
    )

    def __repr__(self) -> str:
        return f"<Assignment(id={self.id}, user_id={self.user_id}, task_id={self.task_id}, status={self.status})>"
