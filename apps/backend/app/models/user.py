"""
Модель пользователя для системы психолог-бота.
"""

from datetime import datetime
from typing import List
import uuid
import enum
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserRole(str, enum.Enum):
    """Роли пользователей в системе."""
    USER = "user"
    ADMIN = "admin"


class User(Base):
    """
    Модель пользователя системы.

    Attributes:
        id: Уникальный идентификатор пользователя (UUID)
        telegram_id: ID пользователя в Telegram (опционально)
        name: Имя пользователя
        email: Email адрес (уникальный, опционально)
        hashed_password: Хешированный пароль для веб-доступа
        role: Роль пользователя (user/admin)
        is_active: Флаг активности аккаунта
        created_at: Дата и время создания
        updated_at: Дата и время последнего обновления
        assignments: Связь с назначенными заданиями
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=True, index=True)
    hashed_password = Column(String(255), nullable=True)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.USER)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    assignments = relationship("Assignment", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}, email={self.email}, role={self.role})>"
