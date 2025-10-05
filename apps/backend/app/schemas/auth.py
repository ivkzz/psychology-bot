"""
Pydantic схемы для аутентификации и авторизации.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.schemas.user import UserResponse


class TokenResponse(BaseModel):
    """Схема ответа с токенами."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Тип токена")


class LoginRequest(BaseModel):
    """Схема запроса на вход в систему."""
    email: EmailStr = Field(..., description="Email адрес пользователя")
    password: str = Field(..., min_length=6, description="Пароль пользователя")


class RegisterRequest(BaseModel):
    """Схема запроса на регистрацию нового пользователя."""
    name: str = Field(..., min_length=1, max_length=100, description="Имя пользователя")
    email: EmailStr = Field(..., description="Email адрес пользователя")
    password: str = Field(..., min_length=6, max_length=100, description="Пароль (минимум 6 символов)")
    telegram_id: Optional[int] = Field(None, description="ID пользователя в Telegram (опционально)")


class RegisterResponse(BaseModel):
    """Схема ответа при успешной регистрации."""
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    """Схема запроса на обновление access token."""
    refresh_token: str = Field(..., description="JWT refresh token")


class TokenPayload(BaseModel):
    """Схема данных, содержащихся в JWT токене."""
    sub: str = Field(..., description="Subject (обычно user_id)")
    exp: int = Field(..., description="Expiration time (timestamp)")
    type: str = Field(..., description="Тип токена (access или refresh)")
