"""
Pydantic схемы для валидации данных заданий и назначений.
"""

from datetime import datetime, date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.task import TaskDifficulty
from app.models.assignment import AssignmentStatus


# ============ Task Schemas ============

class TaskBase(BaseModel):
    """Базовая схема задания."""
    title: str = Field(..., min_length=1, max_length=200, description="Название задания")
    description: str = Field(..., min_length=1, description="Описание задания")
    category: str = Field(..., min_length=1, max_length=50, description="Категория задания")
    difficulty: TaskDifficulty = Field(TaskDifficulty.MEDIUM, description="Уровень сложности")


class TaskCreate(TaskBase):
    """Схема для создания нового задания."""
    pass


class TaskUpdate(BaseModel):
    """Схема для обновления задания."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    difficulty: Optional[TaskDifficulty] = None


class TaskInDB(TaskBase):
    """Схема задания в БД."""
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class TaskResponse(TaskBase):
    """Схема для ответа API с данными задания."""
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Assignment Schemas ============

class AssignmentBase(BaseModel):
    """Базовая схема назначения задания."""
    user_id: UUID
    task_id: UUID
    assigned_date: Optional[date] = Field(None, description="Дата назначения (NULL = в очереди pending)")


class AssignmentCreate(AssignmentBase):
    """Схема для создания назначения."""
    pass


class AssignmentUpdate(BaseModel):
    """Схема для обновления назначения."""
    status: Optional[AssignmentStatus] = None
    answer_text: Optional[str] = None
    completed_at: Optional[datetime] = None


class AssignmentComplete(BaseModel):
    """Схема для отметки задания как выполненного."""
    answer_text: Optional[str] = Field(None, description="Текстовый ответ пользователя на задание")


class AssignmentInDB(AssignmentBase):
    """Схема назначения в БД."""
    id: UUID
    status: AssignmentStatus
    completed_at: Optional[datetime]
    answer_text: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class AssignmentResponse(BaseModel):
    """Схема для ответа API с данными назначения и связанного задания."""
    id: UUID
    user_id: UUID
    task_id: UUID
    assigned_date: Optional[date]  # Может быть NULL для pending заданий
    status: AssignmentStatus
    completed_at: Optional[datetime]
    answer_text: Optional[str]
    created_at: datetime
    task: TaskResponse  # Вложенные данные задания

    class Config:
        from_attributes = True
