# Frontend TODO - Next.js 15 App Router

## Приоритет 1: Инфраструктура и настройка проекта

- [ ] Инициализировать Next.js 15 проект с TypeScript
  ```bash
  npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
  ```

- [ ] Установить основные зависимости
  - [ ] `@tanstack/react-query` - управление серверным состоянием
  - [ ] `fetch native` - HTTP клиент
  - [ ] `zod` - валидация схем
  - [ ] `react-hook-form` - управление формами
  - [ ] `zustand` - клиентское состояние (опционально)
  - [ ] `date-fns` - работа с датами
  - [ ] `lucide-react` - иконки

- [ ] Настроить shadcn/ui
  ```bash
  npx shadcn-ui@latest init
  ```

- [ ] Создать файл `.env.local`
  ```env
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```

- [ ] Настроить Docker
  - [ ] Создать `Dockerfile` (multi-stage build)
  - [ ] Добавить `.dockerignore`
  - [ ] Интегрировать в `docker-compose.yml`

---

## Приоритет 2: Аутентификация (Auth)

### API Integration

- [ ] Создать API клиент (`lib/api/client.ts`)
  - [ ] Axios/Ky instance с базовым URL
  - [ ] Interceptors для JWT токенов
  - [ ] Автоматическое обновление access token через refresh token
  - [ ] Обработка ошибок (401, 403, 500)

- [ ] Создать API методы для auth (`lib/api/auth.ts`)
  - [ ] `POST /api/v1/auth/register` - регистрация
  - [ ] `POST /api/v1/auth/login` - вход
  - [ ] `POST /api/v1/auth/refresh` - обновление токена
  - [ ] `POST /api/v1/auth/logout` - выход

### Auth Context

- [ ] Создать AuthContext (`lib/auth/context.tsx`)
  - [ ] Хранение текущего пользователя
  - [ ] Методы: login, logout, register, refreshToken
  - [ ] Автоматическая проверка токена при загрузке

- [ ] Создать AuthProvider (`lib/auth/provider.tsx`)
  - [ ] Обертка приложения в context
  - [ ] Загрузка пользователя из localStorage/cookies
  - [ ] Automatic token refresh

### Auth Pages

- [ ] Страница входа `app/(unauth)/login/page.tsx`
  - [ ] Форма: email, password
  - [ ] Валидация через react-hook-form + zod
  - [ ] Обработка ошибок (неверный пароль, пользователь не найден)
  - [ ] Редирект после успешного входа → `/dashboard`
  - [ ] Ссылка на регистрацию

- [ ] Страница регистрации `app/(unauth)/register/page.tsx`
  - [ ] Форма: name, email, password, confirmPassword
  - [ ] Валидация паролей (минимум 8 символов, совпадение)
  - [ ] Обработка ошибок (email уже существует)
  - [ ] Редирект после регистрации → `/dashboard`
  - [ ] Ссылка на вход

### Middleware

- [ ] Создать middleware (`middleware.ts`)
  - [ ] Проверка наличия JWT токена
  - [ ] Защита роутов `/dashboard/*`, `/admin/*`
  - [ ] Редирект неавторизованных → `/login`
  - [ ] Проверка роли для админ-панели

---

## Приоритет 3: Пользовательский кабинет

### Dashboard (главная страница)

- [ ] `app/(auth)/dashboard/page.tsx`
  - [ ] Приветствие пользователя (имя)
  - [ ] Карточка с текущим заданием на сегодня
  - [ ] Кнопка "Выполнить задание"
  - [ ] Краткая статистика (выполнено заданий, текущая серия)
  - [ ] Ссылки на историю и полную статистику

### Задания

- [ ] `app/(auth)/tasks/page.tsx` - список заданий
  - [ ] Получение заданий: `GET /api/v1/tasks/today`
  - [ ] Отображение текущего задания
  - [ ] История выполненных заданий (последние 7 дней)
  - [ ] Фильтрация по статусу (pending/completed)

- [ ] Компонент TaskCard (`components/tasks/TaskCard.tsx`)
  - [ ] Название, описание, категория, сложность
  - [ ] Статус (pending/completed)
  - [ ] Кнопка "Выполнить" / "Завершено"
  - [ ] Дата назначения

- [ ] Модальное окно выполнения задания (`components/tasks/CompleteTaskModal.tsx`)
  - [ ] Textarea для ответа пользователя
  - [ ] Отправка: `POST /api/v1/tasks/{id}/complete`
  - [ ] Закрытие после успеха
  - [ ] Toast уведомление

### История

- [ ] `app/(auth)/history/page.tsx`
  - [ ] Получение истории: `GET /api/v1/tasks/history?limit=50&offset=0`
  - [ ] Таблица/список заданий с пагинацией
  - [ ] Фильтры: дата, категория, статус
  - [ ] Сортировка по дате
  - [ ] Детальный просмотр задания (модальное окно)

### Статистика

- [ ] `app/(auth)/stats/page.tsx`
  - [ ] Получение: `GET /api/v1/users/me/progress`
  - [ ] Карточки:
    - [ ] Всего заданий
    - [ ] Выполнено заданий
    - [ ] Процент выполнения
    - [ ] Текущая серия дней
    - [ ] Рекорд серии
  - [ ] График выполнения за месяц (recharts)
  - [ ] Диаграмма по категориям

### Профиль

- [ ] `app/(auth)/profile/page.tsx`
  - [ ] Просмотр данных: `GET /api/v1/users/me`
  - [ ] Форма редактирования: имя, email
  - [ ] Обновление: `PATCH /api/v1/users/me`
  - [ ] Смена пароля (опционально)
  - [ ] Удаление аккаунта (опционально, с подтверждением)

---

## Приоритет 4: Админ-панель

### Защита админ роутов

- [ ] Middleware проверка `role === 'admin'`
- [ ] Редирект не-админов → `/dashboard`

### Список пользователей

- [ ] `app/(auth)/admin/users/page.tsx`
  - [ ] Получение: `GET /api/v1/admin/users?limit=50&offset=0`
  - [ ] Таблица с пользователями:
    - [ ] ID, имя, email, telegram_id, роль, дата регистрации
  - [ ] Пагинация
  - [ ] Поиск по email/имени
  - [ ] Фильтр по роли (user/admin)
  - [ ] Кнопка "Просмотр" → детали пользователя

### Детали пользователя

- [ ] `app/(auth)/admin/users/[id]/page.tsx`
  - [ ] Получение: `GET /api/v1/admin/users/{id}`
  - [ ] Отображение всех данных пользователя
  - [ ] История заданий пользователя
  - [ ] Статистика пользователя
  - [ ] Назначить задание вручную: `POST /api/v1/admin/users/{id}/assign-task`

### Управление шаблонами заданий

- [ ] `app/(auth)/admin/tasks/page.tsx`
  - [ ] Получение: `GET /api/v1/admin/tasks/templates`
  - [ ] Таблица шаблонов:
    - [ ] Название, категория, сложность, дата создания
  - [ ] CRUD операции:
    - [ ] Создать: `POST /api/v1/admin/tasks/templates`
    - [ ] Редактировать: `PATCH /api/v1/admin/tasks/templates/{id}`
    - [ ] Удалить: `DELETE /api/v1/admin/tasks/templates/{id}`

- [ ] Модальное окно создания/редактирования задания
  - [ ] Форма: title, description, category, difficulty
  - [ ] Валидация через zod
  - [ ] Preview шаблона

### Дашборд админа

- [ ] `app/(auth)/admin/page.tsx`
  - [ ] Общая статистика:
    - [ ] Всего пользователей
    - [ ] Активных пользователей (выполнили задание за последние 7 дней)
    - [ ] Всего заданий (шаблонов)
    - [ ] Выполнено заданий сегодня
  - [ ] Графики:
    - [ ] Регистрации по дням
    - [ ] Выполнения по дням
    - [ ] Популярные категории заданий

---

## Приоритет 5: UI/UX компоненты

### Layout компоненты

- [ ] `components/layout/Header.tsx`
  - [ ] Логотип
  - [ ] Навигация (Dashboard, Tasks, History, Stats)
  - [ ] Dropdown меню пользователя (Профиль, Выход)
  - [ ] Индикатор роли (админ badge)

- [ ] `components/layout/Sidebar.tsx` (опционально)
  - [ ] Навигация по разделам
  - [ ] Свернуть/развернуть
  - [ ] Активный пункт меню

- [ ] `components/layout/Footer.tsx`
  - [ ] Copyright
  - [ ] Ссылки (Помощь, Контакты)

### shadcn/ui компоненты

- [ ] Установить и настроить компоненты:
  - [ ] `Button` - кнопки
  - [ ] `Input`, `Textarea` - формы
  - [ ] `Card` - карточки
  - [ ] `Table` - таблицы
  - [ ] `Dialog` - модальные окна
  - [ ] `Select` - выпадающие списки
  - [ ] `Badge` - бейджи
  - [ ] `Tabs` - табы
  - [ ] `Alert` - уведомления
  - [ ] `Skeleton` - загрузка
  - [ ] `Toast` - всплывающие уведомления
  - [ ] `Avatar` - аватары
  - [ ] `Dropdown Menu` - выпадающие меню
  - [ ] `Pagination` - пагинация

### Утилиты

- [ ] `lib/utils/formatters.ts`
  - [ ] formatDate(date) - форматирование дат
  - [ ] formatProgress(completed, total) - процент выполнения
  - [ ] formatStreak(days) - форматирование серии

- [ ] `lib/utils/validators.ts`
  - [ ] Zod схемы для форм (login, register, task, etc.)

- [ ] `lib/hooks/useAuth.ts`
  - [ ] Хук для доступа к auth context

- [ ] `lib/hooks/useUser.ts`
  - [ ] Хук для получения текущего пользователя
  - [ ] TanStack Query integration

---

## Приоритет 6: Дополнительные фичи

### Уведомления

- [ ] Toast notifications для всех действий
  - [ ] Успешный вход/регистрация
  - [ ] Выполнение задания
  - [ ] Ошибки API
  - [ ] Сохранение данных

### Responsive дизайн

- [ ] Адаптив для мобильных устройств
  - [ ] Мобильное меню (burger menu)
  - [ ] Адаптивная таблица (horizontal scroll или cards)
  - [ ] Touch-friendly кнопки

### Dark Mode (опционально)

- [ ] Переключатель темной/светлой темы
- [ ] Сохранение предпочтения в localStorage
- [ ] next-themes интеграция

### Интернационализация (опционально)

- [ ] `next-intl` для мультиязычности
- [ ] Русский (по умолчанию)
- [ ] Английский
- [ ] Переключатель языка в header

### PWA (опционально)

- [ ] `next-pwa` для Progressive Web App
- [ ] Service Worker
- [ ] Offline support
- [ ] Иконки для установки

---

## Приоритет 7: Тестирование и оптимизация

### Тестирование

- [ ] Настроить Jest + React Testing Library
- [ ] Unit тесты для утилит
- [ ] Integration тесты для компонентов
- [ ] E2E тесты с Playwright/Cypress (опционально)

### Оптимизация

- [ ] Lazy loading для тяжелых компонентов
- [ ] Image optimization (next/image)
- [ ] Code splitting
- [ ] Bundle analyzer
- [ ] Lighthouse audit (90+ score)

### SEO

- [ ] Metadata для всех страниц
- [ ] Open Graph теги
- [ ] robots.txt
- [ ] sitemap.xml

---

## Приоритет 8: Deployment

### Конфигурация

- [ ] Dockerfile для production build
- [ ] docker-compose интеграция
- [ ] Environment variables
- [ ] Health check endpoint

### CI/CD (опционально)

- [ ] GitHub Actions для автоматической сборки
- [ ] Автоматический деплой при push в main
- [ ] Линтинг и тесты в CI

---

## Технические детали

### Структура папок

```
apps/frontend/
├── app/
│   ├── (auth)/              # Защищенные маршруты
│   │   ├── layout.tsx
│   │   ├── dashboard/
│   │   ├── tasks/
│   │   ├── history/
│   │   ├── stats/
│   │   ├── profile/
│   │   └── admin/
│   ├── (unauth)/            # Публичные маршруты
│   │   ├── login/
│   │   └── register/
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/                  # shadcn/ui компоненты
│   ├── layout/              # Header, Footer, Sidebar
│   ├── auth/                # Auth-related компоненты
│   ├── tasks/               # Task-related компоненты
│   └── admin/               # Admin-related компоненты
├── lib/
│   ├── api/                 # API клиент
│   ├── auth/                # Auth context/provider
│   ├── hooks/               # Custom hooks
│   └── utils/               # Утилиты
├── types/                   # TypeScript типы
├── public/                  # Статические файлы
├── styles/                  # Глобальные стили
├── .env.local               # Локальные переменные окружения
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── Dockerfile
└── package.json
```

### TypeScript типы (базовые)

```typescript
// types/user.ts
export interface User {
  id: string;
  name: string;
  email: string;
  telegram_id?: number;
  role: 'user' | 'admin';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// types/task.ts
export interface Task {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: 'easy' | 'medium' | 'hard';
  created_at: string;
}

export interface Assignment {
  id: string;
  user_id: string;
  task_id: string;
  assigned_date: string;
  completed_at?: string;
  status: 'pending' | 'completed';
  answer_text?: string;
  task: Task;
}

// types/auth.ts
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
  telegram_id?: number;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}
```

---

## Приоритеты выполнения (рекомендуемый порядок)

1. **Неделя 1:** Приоритет 1-2 (инфраструктура + аутентификация)
2. **Неделя 2:** Приоритет 3 (пользовательский кабинет)
3. **Неделя 3:** Приоритет 4 (админ-панель)
4. **Неделя 4:** Приоритет 5-6 (UI/UX + доп. фичи)
5. **Неделя 5:** Приоритет 7-8 (тестирование + deployment)

---

## Полезные ссылки

- [Next.js 15 Docs](https://nextjs.org/docs)
- [shadcn/ui](https://ui.shadcn.com/)
- [TanStack Query](https://tanstack.com/query/latest)
- [React Hook Form](https://react-hook-form.com/)
- [Zod](https://zod.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Recharts](https://recharts.org/)

---

**Создано:** 2025-10-05
**Статус:** Готово к разработке
**Предварительная оценка:** 4-5 недель на полную реализацию
