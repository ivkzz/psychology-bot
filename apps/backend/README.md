# Backend API для психолог-бота

Полноценный REST API на FastAPI для системы психологических упражнений и заданий.

## Структура проекта

```
apps/backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py          # Аутентификация (регистрация, вход, refresh)
│   │       │   ├── users.py         # Управление пользователями
│   │       │   ├── tasks.py         # Работа с заданиями
│   │       │   └── admin.py         # Админ панель
│   │       └── dependencies.py      # Зависимости (get_current_user, etc.)
│   ├── core/
│   │   ├── config.py                # Настройки приложения
│   │   ├── database.py              # Подключение к БД
│   │   └── security.py              # JWT, хеширование паролей
│   ├── crud/
│   │   ├── user.py                  # CRUD для пользователей
│   │   ├── task.py                  # CRUD для заданий
│   │   └── assignment.py            # CRUD для назначений
│   ├── models/
│   │   ├── user.py                  # SQLAlchemy модель User
│   │   ├── task.py                  # SQLAlchemy модель Task
│   │   └── assignment.py            # SQLAlchemy модель Assignment
│   ├── schemas/
│   │   ├── user.py                  # Pydantic схемы для пользователей
│   │   ├── task.py                  # Pydantic схемы для заданий
│   │   └── auth.py                  # Pydantic схемы для аутентификации
│   ├── services/
│   │   ├── auth_service.py          # Бизнес-логика аутентификации
│   │   ├── task_service.py          # Бизнес-логика заданий
│   │   └── notification_service.py  # Сервис уведомлений (заглушка)
│   └── main.py                      # Точка входа FastAPI
├── alembic/
│   ├── versions/
│   │   └── 001_initial_schema.py    # Начальная миграция + seed данные
│   └── env.py                       # Конфигурация Alembic
├── tests/                           # Тесты (pytest)
├── alembic.ini                      # Конфигурация миграций
├── Dockerfile                       # Docker образ
└── requirements.txt                 # Зависимости Python
```

## Структура базы данных

### Таблица `users`
- **id** (UUID) - первичный ключ
- **telegram_id** (BigInt) - ID пользователя в Telegram (опционально, уникальный)
- **name** (String) - имя пользователя
- **email** (String) - email адрес (опционально, уникальный)
- **hashed_password** (String) - хешированный пароль
- **role** (Enum: USER/ADMIN) - роль пользователя
- **is_active** (Boolean) - активность аккаунта
- **created_at** (DateTime) - дата создания
- **updated_at** (DateTime) - дата обновления

### Таблица `tasks`
- **id** (UUID) - первичный ключ
- **title** (String) - название задания
- **description** (Text) - описание упражнения
- **category** (String) - категория (медитация, дыхание, дневник, etc.)
- **difficulty** (Enum: EASY/MEDIUM/HARD) - уровень сложности
- **created_at** (DateTime) - дата создания

### Таблица `assignments`
- **id** (UUID) - первичный ключ
- **user_id** (UUID) - FK к users (CASCADE DELETE)
- **task_id** (UUID) - FK к tasks (CASCADE DELETE)
- **assigned_date** (Date) - дата назначения
- **completed_at** (DateTime) - дата выполнения (nullable)
- **status** (Enum: PENDING/COMPLETED) - статус
- **answer_text** (Text) - текстовый ответ пользователя (nullable)
- **created_at** (DateTime) - дата создания

**Индексы:**
- `(user_id, assigned_date)` - для быстрого поиска заданий по дате
- `(user_id, status)` - для фильтрации по статусу

## API Endpoints

### Аутентификация (`/api/v1/auth`)

#### `POST /api/v1/auth/register`
Регистрация нового пользователя.

**Request:**
```json
{
  "name": "Иван Иванов",
  "email": "ivan@example.com",
  "password": "password123",
  "telegram_id": 123456789
}
```

**Response (201):**
```json
{
  "user": {
    "id": "uuid",
    "name": "Иван Иванов",
    "email": "ivan@example.com",
    "telegram_id": 123456789,
    "role": "user",
    "is_active": true,
    "created_at": "2025-10-05T10:00:00",
    "updated_at": "2025-10-05T10:00:00"
  },
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### `POST /api/v1/auth/login`
Вход в систему.

**Request:**
```json
{
  "email": "ivan@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### `POST /api/v1/auth/refresh`
Обновление access token.

**Request:**
```json
{
  "refresh_token": "eyJhbGc..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Пользователи (`/api/v1/users`)

#### `GET /api/v1/users/me`
Получить данные текущего пользователя.

**Headers:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "id": "uuid",
  "name": "Иван Иванов",
  "email": "ivan@example.com",
  "telegram_id": 123456789,
  "role": "user",
  "is_active": true,
  "created_at": "2025-10-05T10:00:00",
  "updated_at": "2025-10-05T10:00:00"
}
```

#### `PATCH /api/v1/users/me`
Обновить данные пользователя.

**Headers:** `Authorization: Bearer <access_token>`

**Request:**
```json
{
  "name": "Новое Имя",
  "email": "new@example.com"
}
```

#### `GET /api/v1/users/me/progress`
Получить статистику прогресса.

**Headers:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "total_tasks": 10,
  "completed_tasks": 7,
  "completion_rate": 70.0,
  "streak_days": 5
}
```

### Задания (`/api/v1/tasks`)

#### `GET /api/v1/tasks/today`
Получить задание на сегодня (создает автоматически, если не существует).

**Headers:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "task_id": "uuid",
  "assigned_date": "2025-10-05",
  "status": "pending",
  "completed_at": null,
  "answer_text": null,
  "created_at": "2025-10-05T10:00:00",
  "task": {
    "id": "uuid",
    "title": "Утренняя медитация осознанности",
    "description": "Найдите тихое место...",
    "category": "медитация",
    "difficulty": "easy",
    "created_at": "2025-10-05T10:00:00"
  }
}
```

#### `POST /api/v1/tasks/{assignment_id}/complete`
Отметить задание как выполненное.

**Headers:** `Authorization: Bearer <access_token>`

**Request:**
```json
{
  "answer_text": "Отличное упражнение! Почувствовал себя спокойнее."
}
```

**Response (200):** Обновленное назначение с `status: "completed"`.

#### `GET /api/v1/tasks/history?limit=10&offset=0`
Получить историю заданий с пагинацией.

**Headers:** `Authorization: Bearer <access_token>`

**Response (200):** Массив назначений.

### Админ (`/api/v1/admin`) - только для role=ADMIN

#### `GET /api/v1/admin/users?skip=0&limit=100&is_active=true`
Получить список всех пользователей.

#### `GET /api/v1/admin/users/{user_id}`
Получить данные пользователя по ID.

#### `GET /api/v1/admin/tasks/templates`
Получить список шаблонов заданий.

#### `POST /api/v1/admin/tasks/templates`
Создать новый шаблон задания.

**Request:**
```json
{
  "title": "Новое упражнение",
  "description": "Описание упражнения...",
  "category": "медитация",
  "difficulty": "medium"
}
```

#### `PATCH /api/v1/admin/tasks/templates/{task_id}`
Обновить шаблон задания.

#### `DELETE /api/v1/admin/tasks/templates/{task_id}`
Удалить шаблон задания.

#### `POST /api/v1/admin/users/{user_id}/assign-task?task_id={task_id}`
Назначить задание пользователю.

## Настройка и запуск

### 1. Переменные окружения

Создайте файл `.env`:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/psychologist_bot

# Security
SECRET_KEY=your-secret-key-min-32-characters-long-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# App
APP_NAME=Psychology Bot API
DEBUG=true
API_V1_PREFIX=/api/v1

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Optional
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

### 2. Установка зависимостей

```bash
cd apps/backend
pip install -r requirements.txt
```

### 3. Применение миграций

```bash
# Применить все миграции (создает таблицы + добавляет seed данные)
alembic upgrade head
```

**Seed данные включают:**
- 1 администратора: `admin@psychologist-bot.com` / `admin123`
- 15 шаблонов заданий (медитация, дыхание, дневник, аффирмации, физическая активность, самопознание)

### 4. Запуск сервера

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

API будет доступен по адресу: `http://localhost:8000`

Swagger документация: `http://localhost:8000/docs`

ReDoc документация: `http://localhost:8000/redoc`

### 5. Docker (опционально)

```bash
# Build
docker build -t psychologist-bot-backend .

# Run
docker run -p 8000:8000 --env-file .env psychologist-bot-backend
```

## Примеры использования с curl

### Регистрация пользователя

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "test123"
  }'
```

### Вход в систему

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

### Получить задание на сегодня

```bash
curl -X GET http://localhost:8000/api/v1/tasks/today \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Отметить задание как выполненное

```bash
curl -X POST http://localhost:8000/api/v1/tasks/{assignment_id}/complete \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "answer_text": "Упражнение выполнено успешно!"
  }'
```

### Получить статистику прогресса

```bash
curl -X GET http://localhost:8000/api/v1/users/me/progress \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Тестирование

```bash
# Запуск всех тестов
pytest

# С покрытием
pytest --cov=app --cov-report=html

# Конкретный файл
pytest tests/test_auth.py -v
```

## Основные технологии

- **FastAPI** - современный async веб-фреймворк
- **SQLAlchemy 2.0** - ORM с async поддержкой
- **Alembic** - миграции базы данных
- **Pydantic v2** - валидация данных
- **PostgreSQL** - основная БД
- **JWT** - токены аутентификации (python-jose)
- **Bcrypt** - хеширование паролей (passlib)
- **asyncpg** - async драйвер для PostgreSQL

## Troubleshooting

### Ошибка подключения к БД

Убедитесь, что PostgreSQL запущен и DATABASE_URL в `.env` корректен.

### Миграции не применяются

```bash
# Проверить текущую версию
alembic current

# Посмотреть историю
alembic history

# Откатить миграцию
alembic downgrade -1
```

### JWT токены не работают

Проверьте, что SECRET_KEY установлен в `.env` и длиной минимум 32 символа.

## Roadmap

- [ ] Интеграция с Telegram Bot API для реальных уведомлений
- [ ] Планировщик (APScheduler/Celery) для автоматических заданий
- [ ] Rate limiting (slowapi)
- [ ] Blacklist для отозванных JWT токенов (Redis)
- [ ] Websocket для real-time уведомлений
- [ ] Админ панель (React Admin / Django Admin)
- [ ] Экспорт прогресса в PDF/Excel
- [ ] AI анализ ответов пользователей (OpenAI/Anthropic)

## Лицензия

MIT
