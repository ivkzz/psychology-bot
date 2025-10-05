# Схема базы данных Psychology Bot

## ER-диаграмма (текстовое представление)

```
┌─────────────────────────────────────┐
│           USERS                     │
├─────────────────────────────────────┤
│ PK id: UUID                         │
│    telegram_id: BigInt (UNIQUE)     │
│    name: String(100)                │
│    email: String(255) (UNIQUE)      │
│    hashed_password: String(255)     │
│    role: Enum(USER, ADMIN)          │
│    is_active: Boolean               │
│    created_at: DateTime             │
│    updated_at: DateTime             │
└─────────────────────────────────────┘
            │
            │ 1:N
            │
            ▼
┌─────────────────────────────────────┐
│       ASSIGNMENTS                   │
├─────────────────────────────────────┤
│ PK id: UUID                         │
│ FK user_id: UUID (CASCADE DELETE)   │
│ FK task_id: UUID (CASCADE DELETE)   │
│    assigned_date: Date              │
│    completed_at: DateTime (NULL)    │
│    status: Enum(PENDING, COMPLETED) │
│    answer_text: Text (NULL)         │
│    created_at: DateTime             │
│                                     │
│ IDX (user_id, assigned_date)        │
│ IDX (user_id, status)               │
└─────────────────────────────────────┘
            ▲
            │ N:1
            │
┌─────────────────────────────────────┐
│           TASKS                     │
├─────────────────────────────────────┤
│ PK id: UUID                         │
│    title: String(200)               │
│    description: Text                │
│    category: String(50)             │
│    difficulty: Enum(EASY/MED/HARD)  │
│    created_at: DateTime             │
└─────────────────────────────────────┘
```

## Таблицы

### 1. USERS

**Описание:** Хранит информацию о пользователях системы.

| Колонка          | Тип              | Ограничения                  | Описание                                |
|------------------|------------------|------------------------------|-----------------------------------------|
| id               | UUID             | PRIMARY KEY                  | Уникальный идентификатор                |
| telegram_id      | BigInt           | UNIQUE, NULL                 | ID пользователя в Telegram              |
| name             | String(100)      | NOT NULL                     | Имя пользователя                        |
| email            | String(255)      | UNIQUE, NULL                 | Email адрес                             |
| hashed_password  | String(255)      | NULL                         | Bcrypt хеш пароля                       |
| role             | Enum             | NOT NULL, DEFAULT 'USER'     | Роль: USER или ADMIN                    |
| is_active        | Boolean          | NOT NULL, DEFAULT true       | Активность аккаунта                     |
| created_at       | DateTime         | NOT NULL, DEFAULT now()      | Дата создания                           |
| updated_at       | DateTime         | NOT NULL, DEFAULT now()      | Дата последнего обновления              |

**Индексы:**
- PRIMARY KEY на `id`
- UNIQUE на `telegram_id`
- UNIQUE на `email`

**Связи:**
- 1:N с `assignments` (CASCADE DELETE)

---

### 2. TASKS

**Описание:** Шаблоны упражнений для переиспользования.

| Колонка      | Тип              | Ограничения              | Описание                                |
|--------------|------------------|--------------------------|-----------------------------------------|
| id           | UUID             | PRIMARY KEY              | Уникальный идентификатор                |
| title        | String(200)      | NOT NULL                 | Название упражнения                     |
| description  | Text             | NOT NULL                 | Подробное описание                      |
| category     | String(50)       | NOT NULL                 | Категория (медитация, дыхание и т.д.)   |
| difficulty   | Enum             | NOT NULL, DEFAULT 'MEDIUM' | Уровень сложности                     |
| created_at   | DateTime         | NOT NULL, DEFAULT now()  | Дата создания                           |

**Индексы:**
- PRIMARY KEY на `id`
- INDEX на `category` (для фильтрации)

**Связи:**
- 1:N с `assignments` (CASCADE DELETE)

**Категории:**
- `медитация` - упражнения на осознанность
- `дыхание` - дыхательные техники
- `дневник` - ведение дневника
- `аффирмации` - позитивные утверждения
- `физическая_активность` - физические упражнения
- `самопознание` - исследование себя

**Уровни сложности:**
- `EASY` - легкие упражнения (5-10 минут)
- `MEDIUM` - средние упражнения (10-20 минут)
- `HARD` - сложные упражнения (20+ минут)

---

### 3. ASSIGNMENTS

**Описание:** Назначения заданий пользователям. Связь Many-to-Many между Users и Tasks с дополнительными полями.

| Колонка        | Тип              | Ограничения                  | Описание                                |
|----------------|------------------|------------------------------|-----------------------------------------|
| id             | UUID             | PRIMARY KEY                  | Уникальный идентификатор                |
| user_id        | UUID             | FK to users, NOT NULL        | Пользователь                            |
| task_id        | UUID             | FK to tasks, NOT NULL        | Задание                                 |
| assigned_date  | Date             | NOT NULL, DEFAULT today()    | Дата назначения                         |
| completed_at   | DateTime         | NULL                         | Дата и время выполнения                 |
| status         | Enum             | NOT NULL, DEFAULT 'PENDING'  | Статус выполнения                       |
| answer_text    | Text             | NULL                         | Текстовый ответ пользователя            |
| created_at     | DateTime         | NOT NULL, DEFAULT now()      | Дата создания записи                    |

**Индексы:**
- PRIMARY KEY на `id`
- COMPOSITE INDEX на `(user_id, assigned_date)` - быстрый поиск заданий по дате
- COMPOSITE INDEX на `(user_id, status)` - фильтрация по статусу
- INDEX на `assigned_date` - сортировка по дате

**Связи:**
- N:1 с `users` (CASCADE DELETE - при удалении пользователя удаляются его назначения)
- N:1 с `tasks` (CASCADE DELETE - при удалении задания удаляются назначения)

**Статусы:**
- `PENDING` - задание назначено, но не выполнено
- `COMPLETED` - задание выполнено

---

## Примеры запросов

### Получить все задания пользователя за последние 7 дней

```sql
SELECT a.*, t.title, t.description, t.category
FROM assignments a
JOIN tasks t ON a.task_id = t.id
WHERE a.user_id = 'user-uuid'
  AND a.assigned_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY a.assigned_date DESC;
```

### Подсчитать процент выполнения для пользователя

```sql
SELECT
  COUNT(*) as total_tasks,
  SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) as completed_tasks,
  ROUND(
    100.0 * SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) as completion_rate
FROM assignments
WHERE user_id = 'user-uuid';
```

### Получить случайное задание определенной категории

```sql
SELECT *
FROM tasks
WHERE category = 'медитация'
ORDER BY RANDOM()
LIMIT 1;
```

### Найти пользователей с streak > 5 дней

```sql
WITH daily_completions AS (
  SELECT
    user_id,
    assigned_date,
    LAG(assigned_date) OVER (PARTITION BY user_id ORDER BY assigned_date) as prev_date
  FROM assignments
  WHERE status = 'COMPLETED'
)
SELECT user_id, COUNT(*) as streak_days
FROM daily_completions
WHERE prev_date IS NULL OR assigned_date = prev_date + INTERVAL '1 day'
GROUP BY user_id
HAVING COUNT(*) > 5;
```

## Миграции

### Создание новой миграции

```bash
# Автогенерация на основе изменений моделей
alembic revision --autogenerate -m "описание изменений"

# Создание пустой миграции
alembic revision -m "описание изменений"
```

### Применение миграций

```bash
# Применить все миграции
alembic upgrade head

# Применить следующую миграцию
alembic upgrade +1

# Применить до конкретной версии
alembic upgrade <revision_id>
```

### Откат миграций

```bash
# Откатить последнюю миграцию
alembic downgrade -1

# Откатить до конкретной версии
alembic downgrade <revision_id>

# Откатить все миграции
alembic downgrade base
```

### Просмотр истории

```bash
# Текущая версия
alembic current

# История миграций
alembic history

# Подробная информация
alembic show <revision_id>
```

## Seed данные

Начальная миграция `001_initial_schema.py` включает:

1. **Администратор:**
   - Email: `admin@psychologist-bot.com`
   - Пароль: `admin123`
   - Роль: ADMIN

2. **15 шаблонов заданий:**
   - 3 медитации (easy, easy, medium)
   - 3 дыхательных упражнения (easy, easy, medium)
   - 3 задания по дневнику (easy, medium, hard)
   - 2 аффирмации (easy, medium)
   - 2 физические активности (easy, easy)
   - 2 задания на самопознание (medium, hard)

## Оптимизация производительности

### Индексы

Все критичные поля проиндексированы:
- `users.telegram_id` - для быстрого поиска по Telegram ID
- `users.email` - для быстрого поиска по email
- `tasks.category` - для фильтрации по категориям
- `assignments(user_id, assigned_date)` - для получения заданий по дате
- `assignments(user_id, status)` - для фильтрации по статусу

### Connection Pooling

SQLAlchemy настроен с пулом соединений:
- `pool_size=5` - базовое количество соединений
- `max_overflow=10` - дополнительные соединения при нагрузке
- `pool_pre_ping=True` - проверка соединения перед использованием

### Eager Loading

В CRUD операциях используется `selectinload()` для загрузки связанных данных:

```python
# Загружаем назначение вместе с заданием
select(Assignment).options(selectinload(Assignment.task))
```

## Backup и восстановление

### Создание backup

```bash
pg_dump -U user -d psychologist_bot > backup.sql
```

### Восстановление

```bash
psql -U user -d psychologist_bot < backup.sql
```

## Безопасность

1. **Пароли:** Хешируются с помощью bcrypt (12 раундов)
2. **Cascade Delete:** При удалении пользователя автоматически удаляются его назначения
3. **Foreign Keys:** Обеспечивают целостность данных
4. **Enum типы:** Ограничивают возможные значения для role, status, difficulty
5. **NULL constraints:** Критичные поля обязательны для заполнения
