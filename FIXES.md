# Исправления после детального анализа

## ❌ Найденные проблемы

### 1. **Отсутствует asyncpg драйвер (Backend) - КРИТИЧНО**
**Ошибка:**
```
ModuleNotFoundError: No module named 'asyncpg'
```

**Причина:** SQLAlchemy 2.0 с async поддержкой требует asyncpg драйвер для PostgreSQL.

### 2. **Hardcoded admin credentials в миграции**
**Проблема:** Email и пароль администратора захардкожены в `001_initial_schema.py`.

### 3. **Pydantic @validator устарел**
**Проблема:** В Pydantic 2.x декоратор `@validator` заменен на `@field_validator`.

### 4. **Warning: version в docker-compose**
**Проблема:** Атрибут `version` устарел в Docker Compose v2+.

---

## ✅ Применённые исправления

### 1. **Добавлен asyncpg драйвер**
**Файл:** `apps/backend/requirements.txt`

```diff
# Database
sqlalchemy==2.0.36
alembic==1.14.0
psycopg2-binary==2.9.10
+ asyncpg==0.30.0
```

### 2. **Вынесены admin credentials в конфиг**

**Файл:** `apps/backend/app/core/config.py`
```python
# Seed данные для первого администратора
ADMIN_EMAIL: str = Field(
    default="admin@psychologist-bot.com",
    description="Email администратора для первоначального seed"
)
ADMIN_PASSWORD: str = Field(
    default="admin123",
    description="Пароль администратора (рекомендуется изменить в production)"
)
ADMIN_NAME: str = Field(
    default="Admin",
    description="Имя администратора"
)
```

**Файл:** `.env.example`
```env
# Admin User (для seed данных при первом запуске)
ADMIN_EMAIL=admin@psychologist-bot.com
ADMIN_PASSWORD=admin123
ADMIN_NAME=Admin
```

**Файл:** `apps/backend/alembic/versions/001_initial_schema.py`
```python
from app.core.config import settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Динамическое создание администратора
admin_password_hash = pwd_context.hash(settings.ADMIN_PASSWORD)

op.execute(f"""
    INSERT INTO users (id, name, email, hashed_password, role, is_active, created_at, updated_at)
    VALUES (
        '{uuid.uuid4()}',
        '{settings.ADMIN_NAME}',
        '{settings.ADMIN_EMAIL}',
        '{admin_password_hash}',
        'ADMIN',
        true,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    );
""")
```

### 3. **Обновлен Pydantic validator**

**Файл:** `apps/backend/app/core/config.py`
```python
# Было (Pydantic 1.x):
from pydantic import Field, PostgresDsn, validator

@validator("BACKEND_CORS_ORIGINS", pre=True)
def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
    ...

# Стало (Pydantic 2.x):
from pydantic import Field, PostgresDsn, field_validator

@field_validator("BACKEND_CORS_ORIGINS", mode="before")
@classmethod
def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
    ...
```

### 4. **Удален version из docker-compose**

**Файлы:** `docker-compose.yml`, `docker-compose.dev.yml`
```diff
- version: '3.8'
-
services:
  postgres:
    ...
```

### 5. **Ранее исправленные проблемы**

- ✅ Pydantic Config конфликт (удален вложенный `class Config`)
- ✅ ModuleNotFoundError в Telegram боте (добавлен `PYTHONPATH=/app`)
- ✅ Пояснение про `TELEGRAM_WEBHOOK_URL`

---

## 📋 Следующие шаги для запуска

### 1. Остановить контейнеры

```bash
docker compose -f docker-compose.dev.yml down
```

### 2. Пересобрать Backend (с asyncpg)

```bash
# Только backend (быстрее)
docker compose -f docker-compose.dev.yml build backend

# Или все сервисы
docker compose -f docker-compose.dev.yml build
```

### 3. Настроить .env файл

Создайте/обновите `.env`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:devpassword@postgres:5432/psychology_bot_dev
POSTGRES_USER=postgres
POSTGRES_PASSWORD=devpassword
POSTGRES_DB=psychology_bot_dev

# Backend
SECRET_KEY=$(openssl rand -hex 32)  # Сгенерируйте свой!
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
DEBUG=true
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# Admin User (измените на свои данные!)
ADMIN_EMAIL=your-email@example.com
ADMIN_PASSWORD=your-secure-password
ADMIN_NAME=Your Name

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
BACKEND_API_URL=http://backend:8000
```

**ВАЖНО:**
- `DATABASE_URL` должен использовать `postgresql+asyncpg://`
- Сгенерируйте `SECRET_KEY`: `openssl rand -hex 32`
- Измените `ADMIN_EMAIL` и `ADMIN_PASSWORD`
- Получите `TELEGRAM_BOT_TOKEN` от @BotFather в Telegram

### 4. Запустить все сервисы

```bash
docker compose -f docker-compose.dev.yml up
```

### 5. Применить миграции (создаст таблицы + seed данные)

```bash
docker compose -f docker-compose.dev.yml exec backend alembic upgrade head
```

Это создаст:
- Таблицы: users, tasks, assignments
- Администратора с вашими credentials из .env
- 15 шаблонов психологических заданий

### 6. Проверить работу

```bash
# Health check
curl http://localhost:8000/health

# Должен вернуть: {"status":"healthy"}
```

**Откройте в браузере:**
- Backend API Docs: http://localhost:8000/docs
- PgAdmin: http://localhost:5050 (admin@admin.com / admin)

---

## ✅ Ожидаемые логи после запуска

### PostgreSQL:
```
✅ database system is ready to accept connections
```

### Backend:
```
✅ INFO:     Uvicorn running on http://0.0.0.0:8000
✅ INFO:     Application startup complete.
```

### Telegram Bot:
```
✅ INFO - Telegram bot initialized successfully
✅ INFO - Backend API is available  <-- Теперь должно быть OK!
✅ INFO - Task scheduler started successfully
✅ INFO - Bot is running
```

---

## 🧪 Тестирование

### 1. Вход как администратор (API)

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-secure-password"
  }'
```

Ответ:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Проверить задания

```bash
curl http://localhost:8000/api/v1/admin/tasks/templates \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Должен вернуть список из 15 упражнений.

### 3. Тестирование Telegram бота

1. Откройте Telegram
2. Найдите вашего бота по username
3. Отправьте `/start`
4. Пройдите регистрацию
5. Проверьте `/today`, `/progress`, `/help`

---

## 📂 Список измененных файлов

| Файл | Изменение |
|------|-----------|
| `apps/backend/requirements.txt` | ✅ Добавлен asyncpg + email-validator |
| `apps/telegram-bot/requirements.txt` | ✅ Удален конфликтующий telegram |
| `apps/backend/app/core/config.py` | ✅ field_validator + admin settings |
| `apps/backend/alembic/versions/001_initial_schema.py` | ✅ Динамический admin |
| `.env.example` | ✅ Добавлены ADMIN_* переменные |
| `docker-compose.yml` | ✅ Удален version |
| `docker-compose.dev.yml` | ✅ Удален version |
| `apps/telegram-bot/Dockerfile` | ✅ PYTHONPATH (ранее) |
| `apps/telegram-bot/bot/config.py` | ✅ Удален Config class (ранее) |

## 🔍 Дополнительные проверки зависимостей

### Backend
- ✅ asyncpg (критично) - добавлен для async SQLAlchemy
- ✅ email-validator - добавлен для Pydantic EmailStr
- ✅ Все остальные пакеты проверены

### Telegram Bot
- ✅ Удален `telegram==0.0.1` - конфликтовал с python-telegram-bot
- ✅ Все необходимые пакеты присутствуют

**Подробный отчет:** См. [DEPENDENCIES_CHECK.md](DEPENDENCIES_CHECK.md)

---

## 🎯 Проверочный чеклист

После пересборки и запуска убедитесь:

- [ ] PostgreSQL запущен и принимает подключения
- [ ] Backend доступен на http://localhost:8000
- [ ] Swagger UI работает: http://localhost:8000/docs
- [ ] Миграции применены (15 заданий в БД)
- [ ] Вход как администратор работает
- [ ] Telegram бот запущен и отвечает на команды
- [ ] Backend API доступен для бота

---

**Дата:** 2025-10-05
**Статус:** Все исправления применены, готово к пересборке
**Команда:** `docker compose -f docker-compose.dev.yml down && docker compose -f docker-compose.dev.yml build && docker compose -f docker-compose.dev.yml up`
