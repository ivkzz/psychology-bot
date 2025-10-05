"""
Pydantic схемы для валидации данных пользователей.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.models.user import UserRole


class UserBase(BaseModel):
    """Базовая схема пользователя."""
    name: str = Field(..., min_length=1, max_length=100, description="Имя пользователя")
    email: Optional[EmailStr] = Field(None, description="Email адрес пользователя")
    telegram_id: Optional[int] = Field(None, description="ID пользователя в Telegram")


class UserCreate(UserBase):
    """Схема для создания нового пользователя."""
    password: Optional[str] = Field(None, min_length=6, max_length=100, description="Пароль (минимум 6 символов)")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        """Валидация пароля."""
        if v is not None and len(v) < 6:
            raise ValueError("Пароль должен содержать минимум 6 символов")
        return v


class UserUpdate(BaseModel):
    """Схема для обновления данных пользователя."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    telegram_id: Optional[int] = None


class UserInDB(UserBase):
    """Схема пользователя в БД (с внутренними полями)."""
    id: UUID
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """Схема для ответа API с данными пользователя."""
    id: UUID
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProgress(BaseModel):
    """Схема для статистики прогресса пользователя."""
    total_tasks: int = Field(..., description="Общее количество назначенных заданий")
    completed_tasks: int = Field(..., description="Количество выполненных заданий")
    completion_rate: float = Field(..., ge=0, le=100, description="Процент выполнения заданий")
    streak_days: int = Field(0, ge=0, description="Количество дней подряд с выполненными заданиями")

    class Config:
        from_attributes = True
