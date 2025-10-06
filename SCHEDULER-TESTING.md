# Тестирование Планировщика (Scheduler)

## 📌 Как работает планировщик

Планировщик автоматически запускается в **Backend** при старте и выполняет задачи по расписанию:
- **Утренние задания**: Каждый день в `MORNING_TASK_TIME` (по умолчанию 09:00)
- **Вечерние напоминания**: Каждый день в `EVENING_REMINDER_TIME` (по умолчанию 20:00)

Планировщик отправляет сообщения напрямую в Telegram через Bot API.

---

## 🧪 Способ 1: Изменить время в `.env` (для автоматического теста)

### Шаг 1: Узнать текущее время на сервере

```bash
# Linux/Mac
docker compose -f docker-compose.dev.yml exec backend date +"%H:%M"

# Windows
docker compose -f docker-compose.dev.yml exec backend date /t && docker compose -f docker-compose.dev.yml exec backend time /t
```

### Шаг 2: Изменить время в `.env`

Откройте файл `.env` и измените время на **2-3 минуты вперед** от текущего:

```env
# Если сейчас 14:30, установите:
MORNING_TASK_TIME=14:32
EVENING_REMINDER_TIME=20:00
```

### Шаг 3: Перезапустить backend

**Linux/Mac:**
```bash
./restart-scheduler.sh
```

**Windows:**
```cmd
restart-scheduler.bat
```

**Или вручную:**
```bash
docker compose -f docker-compose.dev.yml restart backend
```

### Шаг 4: Подождать и проверить логи

Подождите наступления указанного времени (14:32) и проверьте логи:

```bash
# Следить за логами в реальном времени
docker compose -f docker-compose.dev.yml logs backend -f

# Или просмотреть последние логи
docker compose -f docker-compose.dev.yml logs backend --tail 50 | grep -i "morning\|scheduler"
```

**Ожидаемый результат:**
```
INFO:     Starting morning tasks distribution...
INFO:     Morning task sent to user xxx
INFO:     Morning tasks distribution completed: 1 success, 0 errors
```

---

## 📋 Проверка статуса планировщика

### Проверить, что планировщик запущен

```bash
docker compose -f docker-compose.dev.yml logs backend | grep -i "scheduler"
```

**Должно быть:**
```
INFO:     Task scheduler started successfully
INFO:     Task scheduler started successfully. Morning tasks: 09:00, Evening reminders: 20:00
```

### Проверить, что задачи зарегистрированы

```bash
docker compose -f docker-compose.dev.yml logs backend | grep -i "added job"
```

**Должно быть:**
```
INFO:     Added job "Send morning tasks" to job store "default"
INFO:     Added job "Send evening reminders" to job store "default"
```

---

## 🐛 Устранение проблем

### Планировщик не запускается

**Проверьте, что `TELEGRAM_BOT_TOKEN` установлен:**
```bash
docker compose -f docker-compose.dev.yml exec backend env | grep TELEGRAM_BOT_TOKEN
```

Если не установлен, добавьте в `.env`:
```env
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
```

И перезапустите:
```bash
docker compose -f docker-compose.dev.yml restart backend
```

### Задания не отправляются

1. **Проверьте логи backend:**
   ```bash
   docker compose -f docker-compose.dev.yml logs backend --tail 100
   ```

2. **Проверьте, что у пользователей есть telegram_id:**
   - Пользователь должен зарегистрироваться через Telegram бота (`/start`)
   - Только после регистрации у него появится `telegram_id` в БД

3. **Проверьте, что есть активные задания:**
   - В админ-панели на фронте должны быть созданы шаблоны заданий
   - Пользователям должны быть назначены задания

---

## 🔧 Настройки планировщика в `.env`

```env
# Telegram Bot Token (обязательно!)
TELEGRAM_BOT_TOKEN=8456404270:AAHT28bOwSoXQ5fhDRYZd_S0LmjE_8r2TwI

# Временная зона (по умолчанию Europe/Moscow)
SCHEDULER_TIMEZONE=Europe/Moscow

# Время отправки утренних заданий (формат HH:MM)
MORNING_TASK_TIME=09:00

# Время отправки вечерних напоминаний (формат HH:MM)
EVENING_REMINDER_TIME=20:00
```

---

## 📝 Полезные команды

```bash
# Логи backend в реальном времени
docker compose -f docker-compose.dev.yml logs backend -f

# Логи только планировщика
docker compose -f docker-compose.dev.yml logs backend | grep -i scheduler

# Перезапустить backend
docker compose -f docker-compose.dev.yml restart backend

# Полная перезагрузка всех сервисов
docker compose -f docker-compose.dev.yml down && docker compose -f docker-compose.dev.yml up -d

# Проверить статус всех контейнеров
docker compose -f docker-compose.dev.yml ps
```

---

## ✅ Успешный тест

После успешного теста вы должны увидеть:

1. **В логах backend:**
   ```
   INFO:     Starting morning tasks distribution...
   INFO:     Morning task sent to user a0d28763-321c-445b-9807-3618e8b7e4f4
   INFO:     Morning tasks distribution completed: 1 success, 0 errors
   ```

2. **В Telegram:**
   ```
   ☀️ Доброе утро, ИМЯ_ПОЛЬЗОВАТЕЛЯ!

   📋 Ваше задание на сегодня:
   Название задания

   📝 Описание:
   Описание задания

   Используйте команду /today чтобы посмотреть задание и выполнить его.
   ```

3. **Задание можно выполнить:**
   - В боте `/today`
   - Нажать "Выполнить"
   - Отправить текстовый ответ или нажать "Пропустить"
