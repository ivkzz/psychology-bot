# Psychology Bot - Платформа для психологических заданий

Полнофункциональная платформа для управления психологическими заданиями с интеграцией Telegram бота, веб-интерфейсом и RESTful API.

## Описание проекта

Psychology Bot - это комплексное решение для психологов и их клиентов, позволяющее:
- Создавать и управлять психологическими заданиями
- Отправлять задания пользователям через Telegram
- Отслеживать прогресс выполнения заданий
- Управлять пользователями через веб-интерфейс администратора
- Получать напоминания и уведомления

## Технологический стек

### Backend
- **Python 3.11+** - основной язык разработки
- **FastAPI** - современный веб-фреймворк для API
- **SQLAlchemy 2.0** - ORM с поддержкой async
- **PostgreSQL 18** - реляционная база данных
- **Alembic** - система миграций БД
- **JWT** - аутентификация и авторизация

### Telegram Bot
- **python-telegram-bot v21+** - библиотека для Telegram Bot API
- **APScheduler** - планировщик задач для напоминаний
- **httpx** - async HTTP клиент для взаимодействия с Backend API

### Frontend (планируется)
- **Next.js 15** - React фреймворк с App Router
- **TypeScript** - типизированный JavaScript
- **Tailwind CSS** - utility-first CSS фреймворк

### Infrastructure
- **Docker** - контейнеризация приложений
- **docker-compose** - оркестрация контейнеров
- **PostgreSQL 18** - база данных в контейнере

## Структура проекта

```
psychology-bot/
├── apps/
│   ├── backend/              # FastAPI приложение
│   │   ├── app/
│   │   │   ├── api/          # API endpoints
│   │   │   ├── core/         # Конфигурация, БД, безопасность
│   │   │   ├── models/       # SQLAlchemy модели
│   │   │   ├── schemas/      # Pydantic схемы
│   │   │   ├── services/     # Бизнес-логика
│   │   │   ├── crud/         # CRUD операции
│   │   │   └── main.py       # Точка входа
│   │   ├── alembic/          # Миграции БД
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── telegram-bot/         # Telegram бот
│   │   ├── bot/
│   │   │   ├── handlers/     # Обработчики команд
│   │   │   ├── services/     # Сервисы бота
│   │   │   ├── utils/        # Утилиты
│   │   │   ├── config.py     # Конфигурация
│   │   │   └── main.py       # Точка входа
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── frontend/             # Next.js приложение (будет реализовано)
│
├── shared/                   # Общий код
│   ├── constants.py
│   └── utils.py
│
├── scripts/                  # Утилиты
│   ├── dev.sh               # Запуск в dev режиме
│   ├── migrate.sh           # Управление миграциями
│   └── seed-db.sh           # Заполнение тестовыми данными
│
├── docker-compose.yml        # Production конфигурация
├── docker-compose.dev.yml    # Development конфигурация
├── .env.example             # Пример переменных окружения
└── README.md
```

## Быстрый старт

### Предварительные требования

- Docker 20.10+
- Docker Compose 2.0+
- Git

### Установка и запуск

1. **Клонирование репозитория**
```bash
git clone https://github.com/your-org/psychology-bot.git
cd psychology-bot
```

2. **Настройка переменных окружения**
```bash
cp .env.example .env
# Отредактируйте .env файл, добавьте необходимые значения
```

Обязательно настройте следующие переменные:
- `TELEGRAM_BOT_TOKEN` - токен от [@BotFather](https://t.me/botfather)
- `SECRET_KEY` - секретный ключ для JWT (минимум 32 символа)
- `POSTGRES_PASSWORD` - пароль для PostgreSQL

3. **Запуск в production режиме**
```bash
docker compose up -d
```

4. **Запуск в development режиме**
```bash
docker compose -f docker-compose.dev.yml up
# или используйте скрипт:
./scripts/dev.sh
```

5. **Выполнение миграций БД**
```bash
docker compose exec backend alembic upgrade head
# или используйте скрипт:
./scripts/migrate.sh upgrade
```

### Проверка работоспособности

После запуска проверьте доступность сервисов:

- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **PostgreSQL**: localhost:5432
- **PgAdmin (dev)**: http://localhost:5050 (admin@admin.com / admin)

## API Endpoints

### Аутентификация
- `POST /api/v1/auth/register` - Регистрация нового пользователя
- `POST /api/v1/auth/login` - Вход в систему
- `POST /api/v1/auth/refresh` - Обновление токена
- `POST /api/v1/auth/logout` - Выход из системы

### Пользователи
- `GET /api/v1/users/me` - Получить текущего пользователя
- `PUT /api/v1/users/me` - Обновить профиль
- `GET /api/v1/users/{id}` - Получить пользователя по ID (admin)

### Задания
- `GET /api/v1/tasks` - Получить список заданий
- `POST /api/v1/tasks` - Создать новое задание (admin)
- `GET /api/v1/tasks/{id}` - Получить задание по ID
- `PUT /api/v1/tasks/{id}` - Обновить задание (admin)
- `DELETE /api/v1/tasks/{id}` - Удалить задание (admin)
- `POST /api/v1/tasks/{id}/assign` - Назначить задание пользователю (admin)

### Администрирование
- `GET /api/v1/admin/users` - Список всех пользователей
- `GET /api/v1/admin/stats` - Статистика системы
- `PUT /api/v1/admin/users/{id}/role` - Изменить роль пользователя

Полная документация доступна по адресу: http://localhost:8000/docs

## Управление миграциями БД

### Создание новой миграции
```bash
docker compose exec backend alembic revision --autogenerate -m "Description"
# или используйте скрипт:
./scripts/migrate.sh revision "Description"
```

### Применение миграций
```bash
docker compose exec backend alembic upgrade head
# или:
./scripts/migrate.sh upgrade
```

### Откат миграции
```bash
docker compose exec backend alembic downgrade -1
# или:
./scripts/migrate.sh downgrade
```

### История миграций
```bash
./scripts/migrate.sh history
```

## Разработка

### Структура Backend API

- **api/v1/endpoints/** - REST API endpoints
- **core/** - Конфигурация, подключение к БД, безопасность
- **models/** - SQLAlchemy модели (User, Task, Assignment)
- **schemas/** - Pydantic схемы для валидации
- **services/** - Бизнес-логика приложения
- **crud/** - CRUD операции с БД

### Структура Telegram Bot

- **handlers/** - Обработчики команд и сообщений
- **services/api_client.py** - HTTP клиент для взаимодействия с Backend
- **services/scheduler.py** - Планировщик для отправки напоминаний
- **utils/** - Вспомогательные функции

## Переменные окружения

Основные переменные (см. `.env.example` для полного списка):

```env
# Database
DATABASE_URL=postgresql://postgres:password@postgres:5432/psychology_bot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=psychology_bot

# Backend
SECRET_KEY=your-secret-key-min-32-characters-change-in-prod
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
BACKEND_API_URL=http://backend:8000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Безопасность

- Все пароли хешируются с использованием bcrypt
- JWT токены для аутентификации (Access + Refresh)
- CORS настроен для защиты от несанкционированных запросов
- Секреты хранятся в переменных окружения
- Docker контейнеры работают от непривилегированных пользователей

## Логирование

- Backend: логи доступны через `docker compose logs backend`
- Telegram Bot: логи доступны через `docker compose logs telegram-bot`
- PostgreSQL: логи доступны через `docker compose logs postgres`

Просмотр логов в реальном времени:
```bash
docker compose logs -f backend
```

## Тестирование

```bash
# Backend тесты
docker compose exec backend pytest

# С покрытием кода
docker compose exec backend pytest --cov=app --cov-report=html
```

## Deployment в Production

1. Измените все пароли и секретные ключи в `.env`
2. Настройте HTTPS (используйте nginx/traefik с Let's Encrypt)
3. Настройте backup для PostgreSQL
4. Используйте `docker-compose.yml` вместо dev версии
5. Настройте мониторинг (Sentry, Prometheus)
6. Включите rate limiting и другие меры безопасности

## Мониторинг и отладка

### Просмотр запущенных контейнеров
```bash
docker compose ps
```

### Подключение к БД
```bash
docker compose exec postgres psql -U postgres -d psychology_bot
```

### Выполнение команд внутри контейнера
```bash
docker compose exec backend bash
docker compose exec telegram-bot bash
```

## Лицензия

MIT License
