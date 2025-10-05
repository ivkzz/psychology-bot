"""
=8F80;870F8O <>4C;59 Pydantic AE5<.
"""

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserInDB,
    UserResponse,
    UserProgress,
)
from app.schemas.task import (
    TaskBase,
    TaskCreate,
    TaskUpdate,
    TaskInDB,
    TaskResponse,
    AssignmentBase,
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentComplete,
    AssignmentInDB,
    AssignmentResponse,
)
from app.schemas.auth import (
    TokenResponse,
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    RefreshRequest,
    TokenPayload,
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "UserResponse",
    "UserProgress",
    # Task schemas
    "TaskBase",
    "TaskCreate",
    "TaskUpdate",
    "TaskInDB",
    "TaskResponse",
    # Assignment schemas
    "AssignmentBase",
    "AssignmentCreate",
    "AssignmentUpdate",
    "AssignmentComplete",
    "AssignmentInDB",
    "AssignmentResponse",
    # Auth schemas
    "TokenResponse",
    "LoginRequest",
    "RegisterRequest",
    "RegisterResponse",
    "RefreshRequest",
    "TokenPayload",
]
