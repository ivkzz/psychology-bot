# Инструкция по первоначальной настройке проекта

## Шаг 1: Создание .env файла

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

## Шаг 2: Получение Telegram Bot Token

1. Откройте Telegram и найдите [@BotFather](https://t.me/botfather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен
5. Вставьте токен в `.env` файл в параметр `TELEGRAM_BOT_TOKEN`

## Шаг 3: Генерация SECRET_KEY

Для генерации безопасного SECRET_KEY используйте один из способов:

### Способ 1: OpenSSL (Linux/Mac/Windows Git Bash)
```bash
openssl rand -hex 32
```

## Шаг 4: Настройка пароля базы данных

Измените `POSTGRES_PASSWORD` в `.env` файле на безопасный пароль.

**Важно**: Используйте сложный пароль для production!

## Шаг 5: Проверка конфигурации

Убедитесь, что в `.env` файле заполнены следующие обязательные параметры:

- `TELEGRAM_BOT_TOKEN` - токен от BotFather
- `SECRET_KEY` - секретный ключ (минимум 32 символа)
- `POSTGRES_PASSWORD` - пароль для PostgreSQL
- `DATABASE_URL` - должен содержать корректный пароль из `POSTGRES_PASSWORD`

Пример корректной `DATABASE_URL`:
```
DATABASE_URL=postgresql://postgres:your_secure_password@postgres:5432/psychology_bot
```

## Шаг 6: Запуск проекта

### Разработка (Development)

```bash
# Запуск всех сервисов в режиме разработки
docker compose -f docker-compose.dev.yml up

# Или используйте скрипт
chmod +x scripts/dev.sh
./scripts/dev.sh
```

### Production

```bash
# Запуск в фоновом режиме
docker compose up -d

# Просмотр логов
docker compose logs -f
```

## Шаг 7: Выполнение миграций

После первого запуска необходимо применить миграции базы данных:

```bash
# Применить все миграции
docker compose exec backend alembic upgrade head

# Или используйте скрипт
chmod +x scripts/migrate.sh
./scripts/migrate.sh upgrade
```

## Шаг 8: Проверка работоспособности

1. **Backend API**: Откройте http://localhost:8000
   - Должно появиться сообщение: `{"message": "Psychology Bot API", "status": "running"}`

2. **API Документация**: Откройте http://localhost:8000/docs
   - Должна появиться интерактивная Swagger документация

3. **Health Check**: http://localhost:8000/health
   - Должен вернуть статус: `{"status": "healthy"}`

4. **Telegram Bot**: Найдите вашего бота в Telegram и отправьте команду `/start`
   - Бот должен ответить (после реализации handlers)

5. **PgAdmin (dev)**: http://localhost:5050
   - Email: admin@admin.com
   - Password: admin

## Troubleshooting

### Проблема: Контейнеры не запускаются

**Решение**:
```bash
# Остановить все контейнеры
docker compose down

# Пересобрать образы
docker compose build --no-cache

# Запустить снова
docker compose up
```

### Проблема: База данных не подключается

**Решение**:
1. Проверьте, что PostgreSQL контейнер запущен: `docker compose ps`
2. Проверьте логи PostgreSQL: `docker compose logs postgres`
3. Убедитесь, что `DATABASE_URL` в `.env` корректен
4. Проверьте, что пароль в `DATABASE_URL` совпадает с `POSTGRES_PASSWORD`

### Проблема: Telegram Bot не отвечает

**Решение**:
1. Проверьте логи бота: `docker compose logs telegram-bot`
2. Убедитесь, что `TELEGRAM_BOT_TOKEN` корректен
3. Проверьте, что Backend API доступен из контейнера бота
4. Убедитесь, что handlers зарегистрированы в `bot/main.py`

### Проблема: Порт уже занят

**Решение**:
```bash
# Найти процесс, использующий порт (например, 8000)
# Linux/Mac:
lsof -i :8000
# Windows:
netstat -ano | findstr :8000

# Остановить процесс или изменить порт в docker-compose.yml
```

### Проблема: Permission denied на скриптах

**Решение**:
```bash
# Дать права на выполнение всем скриптам
chmod +x scripts/*.sh
```

## Полезные команды

### Docker Compose

```bash
# Просмотр логов конкретного сервиса
docker compose logs backend
docker compose logs telegram-bot
docker compose logs postgres

# Просмотр логов в реальном времени
docker compose logs -f backend

# Остановка всех сервисов
docker compose down

# Остановка и удаление volumes (БД будет очищена!)
docker compose down -v

# Перезапуск конкретного сервиса
docker compose restart backend

# Выполнение команды в контейнере
docker compose exec backend bash
docker compose exec backend python -m pytest
```

### Alembic (миграции)

```bash
# Создать новую миграцию
./scripts/migrate.sh revision "Описание миграции"

# Применить миграции
./scripts/migrate.sh upgrade

# Откатить последнюю миграцию
./scripts/migrate.sh downgrade

# Посмотреть историю миграций
./scripts/migrate.sh history

# Посмотреть текущую версию
./scripts/migrate.sh current
```