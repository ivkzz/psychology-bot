"""
Скрипт для обновления данных администратора из .env файла.
Использование: python scripts/update_admin.py
"""

import asyncio
import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select, update
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash
from app.core.config import settings


async def update_admin():
    """Обновить данные администратора из настроек окружения."""
    async with AsyncSessionLocal() as session:
        # Находим админа
        result = await session.execute(
            select(User).where(User.role == "ADMIN")
        )
        admin = result.scalar_one_or_none()

        if not admin:
            print("❌ Администратор не найден в базе данных!")
            print("💡 Запустите миграции: alembic upgrade head")
            return

        print(f"📌 Найден администратор: {admin.email}")

        # Обновляем данные
        old_email = admin.email
        admin.email = settings.ADMIN_EMAIL
        admin.name = settings.ADMIN_NAME
        admin.hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
        admin.is_active = True

        await session.commit()

        print(f"✅ Администратор обновлен!")
        print(f"   Email: {old_email} → {admin.email}")
        print(f"   Имя: {admin.name}")
        print(f"   Пароль: обновлен из ADMIN_PASSWORD")


if __name__ == "__main__":
    print("🔄 Обновление данных администратора...")
    print(f"   Из .env: ADMIN_EMAIL={settings.ADMIN_EMAIL}")
    print(f"   Из .env: ADMIN_NAME={settings.ADMIN_NAME}")
    print()

    asyncio.run(update_admin())
