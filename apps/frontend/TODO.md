# Frontend TODO - Next.js 15 App Router

## Приоритет 1: Инфраструктура и настройка проекта ✅

- [x] **ГОТОВО:** Инициализировать Next.js 15 проект с TypeScript
- [x] **ГОТОВО:** Установить основные зависимости
  - [x] `@tanstack/react-query` v5.90.2
  - [x] `axios` v1.12.2
  - [x] `zod` v4.1.11
  - [x] `react-hook-form` v7.64.0
  - [x] `@hookform/resolvers` v5.2.2
  - [x] `zustand` v5.0.8
  - [x] `date-fns` v4.1.0
  - [x] `lucide-react` v0.544.0
  - [x] `sonner` v2.0.7
  - [x] `next-themes` v0.4.6
  - [x] `recharts` v2.15.4 (опционально)

- [x] **ГОТОВО:** Настроить shadcn/ui - установлены ВСЕ компоненты (50+)

- [x] **ГОТОВО:** Создать файл `.env.local`

- [x] **ГОТОВО:** Настроить Docker
  - [x] Создать `Dockerfile` (multi-stage build: development, builder, production)
  - [x] Добавить `.dockerignore`
  - [x] Интегрировать в `docker-compose.dev.yml` (development режим)
  - [x] Интегрировать в `docker-compose.yml` (production режим)
  - [x] Настроить `output: "standalone"` в `next.config.ts` для оптимизации

---

## Приоритет 2: Аутентификация (Auth)

### API Integration

- [ ] Создать Axios клиент (`lib/api/client.ts`)
  - [ ] Axios instance с `baseURL` из env
  - [ ] Request interceptor для добавления `Authorization: Bearer {token}`
  - [ ] Response interceptor для обработки 401 (автообновление токена)
  - [ ] Response interceptor для обработки ошибок (403, 500)
  - [ ] Типизация ошибок (ApiError interface)

- [ ] Настроить TanStack Query Provider (`lib/api/query-provider.tsx`)
  - [ ] QueryClient с настройками (staleTime, cacheTime)
  - [ ] QueryClientProvider обертка для app
  - [ ] Devtools для разработки

- [ ] Создать API методы для auth (`lib/api/auth.ts`)
  - [ ] `POST /api/v1/auth/register` → RegisterResponse
  - [ ] `POST /api/v1/auth/login` → TokenResponse
  - [ ] `POST /api/v1/auth/refresh` → TokenResponse
  - [ ] `POST /api/v1/auth/logout` → void (информационный)

- [ ] Создать API методы для users (`lib/api/users.ts`)
  - [ ] `GET /api/v1/users/me` → UserResponse
  - [ ] `PATCH /api/v1/users/me` → UserResponse
  - [ ] `GET /api/v1/users/me/progress` → UserProgress

- [ ] Создать API методы для tasks (`lib/api/tasks.ts`)
  - [ ] `GET /api/v1/tasks/today` → AssignmentResponse
  - [ ] `POST /api/v1/tasks/{id}/complete` → AssignmentResponse
  - [ ] `GET /api/v1/tasks/history?limit&offset` → AssignmentResponse[]

- [ ] Создать API методы для admin (`lib/api/admin.ts`)
  - [ ] `GET /api/v1/admin/users?skip&limit&is_active` → UserResponse[]
  - [ ] `GET /api/v1/admin/users/{id}` → UserResponse
  - [ ] `GET /api/v1/admin/tasks/templates?skip&limit&category&difficulty` → TaskResponse[]
  - [ ] `POST /api/v1/admin/tasks/templates` → TaskResponse
  - [ ] `PATCH /api/v1/admin/tasks/templates/{id}` → TaskResponse
  - [ ] `DELETE /api/v1/admin/tasks/templates/{id}` → void
  - [ ] `POST /api/v1/admin/users/{user_id}/assign-task?task_id` → AssignmentResponse

### Auth Store (Zustand)

- [ ] Создать Auth Store (`lib/stores/auth-store.ts`)
  - [ ] State: accessToken, refreshToken, isAuthenticated
  - [ ] Actions: setTokens, clearTokens, logout
  - [ ] Persist в localStorage (zustand/middleware persist)
  - [ ] **Важно:** НЕ хранить user data (только токены!)

- [ ] Создать Auth Hooks с TanStack Query (`lib/hooks/use-auth.ts`)
  - [ ] `useLogin` mutation - вход в систему (сохраняет токены в Zustand)
  - [ ] `useRegister` mutation - регистрация (сохраняет токены в Zustand)
  - [ ] `useLogout` mutation - выход (очищает токены из Zustand)
  - [ ] `useCurrentUser` query - получение данных пользователя (TanStack Query cache)
  - [ ] `useRefreshToken` mutation - обновление токена (обновляет токены в Zustand)
  - [ ] Интеграция: токены в Zustand, user data в TanStack Query

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
  - [ ] Хук `useTodayTask` для получения задания дня
  - [ ] Отображение текущего задания (карточка с деталями)
  - [ ] Кнопка "Выполнить задание" (открывает модальное окно)
  - [ ] История выполненных заданий (последние 7 дней)
  - [ ] Loading/Error states

- [ ] Компонент TaskCard (`components/tasks/TaskCard.tsx`)
  - [ ] Название, описание, категория, сложность
  - [ ] Badge для статуса (pending/completed) и difficulty
  - [ ] Дата назначения (formatDate)
  - [ ] Conditional rendering: "Выполнить" / "Завершено ✓"
  - [ ] Иконка категории (медитация, дыхание и т.д.)

- [ ] Модальное окно выполнения задания (`components/tasks/CompleteTaskModal.tsx`)
  - [ ] Dialog (shadcn/ui)
  - [ ] Textarea для ответа пользователя (react-hook-form)
  - [ ] Validation: optional answer, max 2000 символов
  - [ ] Mutation `useCompleteTask` для отправки
  - [ ] Optimistic update в TanStack Query
  - [ ] Toast уведомление (sonner) при успехе
  - [ ] Автозакрытие после успеха

### История

- [ ] `app/(auth)/history/page.tsx`
  - [ ] Хук `useTaskHistory(limit, offset)` с TanStack Query
  - [ ] Таблица заданий (shadcn/ui Table) или список карточек
  - [ ] Client-side фильтры: категория, статус (useState)
  - [ ] Пагинация (shadcn/ui Pagination)
  - [ ] Infinite scroll (опционально, useInfiniteQuery)
  - [ ] Клик на задание → модальное окно с деталями
  - [ ] Отображение answer_text для выполненных заданий

### Статистика

- [ ] `app/(auth)/stats/page.tsx`
  - [ ] Хук `useUserProgress` для получения статистики
  - [ ] 4 карточки (Grid layout):
    - [ ] Всего заданий (total_tasks)
    - [ ] Выполнено заданий (completed_tasks)
    - [ ] Процент выполнения (completion_rate) с прогресс-баром (shadcn/ui Progress)
    - [ ] Текущая серия дней (streak_days) с иконкой огня 🔥
  - [ ] Список выполненных заданий по категориям (группировка + подсчет)
    - [ ] Получить историю заданий
    - [ ] Client-side группировка по category (date-fns/lodash)
    - [ ] Отображение в виде списка или таблицы с badges

### Профиль

- [ ] `app/(auth)/profile/page.tsx`
  - [ ] Хук `useCurrentUser` для отображения данных
  - [ ] Форма редактирования (react-hook-form + zod):
    - [ ] name (string, min 1, max 100)
    - [ ] email (EmailStr)
  - [ ] Mutation `useUpdateProfile` для обновления
  - [ ] Optimistic update в TanStack Query
  - [ ] Toast уведомления (успех/ошибка)
  - [ ] Отображение telegram_id (read-only, если есть)
  - [ ] Отображение роли (user/admin badge)
  - [ ] Дата регистрации (created_at)

---

## Приоритет 4: Админ-панель

### Защита админ роутов

- [ ] Middleware проверка `role === 'admin'`
- [ ] Редирект не-админов → `/dashboard`

### Список пользователей

- [ ] `app/(auth)/admin/users/page.tsx`
  - [ ] Хук `useAdminUsers(skip, limit, is_active)` с TanStack Query
  - [ ] Таблица с колонками:
    - [ ] ID (UUID, копировать в буфер)
    - [ ] Имя, Email, Telegram ID
    - [ ] Роль (badge), Статус (is_active)
    - [ ] Дата регистрации
    - [ ] Действия: "Просмотр" кнопка
  - [ ] Client-side поиск по имени/email (useState)
  - [ ] Фильтр: is_active (true/false/all)
  - [ ] Пагинация (skip/limit)
  - [ ] Link на `/admin/users/{id}`

### Детали пользователя

- [ ] `app/(auth)/admin/users/[id]/page.tsx`
  - [ ] Хук `useAdminUserDetails(id)` для получения данных
  - [ ] Секция: Информация о пользователе (Card)
    - [ ] ID, имя, email, telegram_id, роль, is_active
    - [ ] created_at, updated_at
  - [ ] Секция: История заданий (повторное использование TaskCard)
    - [ ] Получить через `useTaskHistory` или отдельный хук
  - [ ] Секция: Статистика пользователя
    - [ ] Мини-версия страницы stats (карточки)
  - [ ] Секция: Назначить задание вручную
    - [ ] Select со списком всех шаблонов (useTaskTemplates)
    - [ ] Mutation `useAssignTask(userId, taskId)`
    - [ ] Toast уведомление при успехе

### Управление шаблонами заданий

- [ ] `app/(auth)/admin/tasks/page.tsx`
  - [ ] Хук `useTaskTemplates(skip, limit, category, difficulty)` с TanStack Query
  - [ ] Таблица/Grid шаблонов:
    - [ ] Название, категория (badge), сложность (badge)
    - [ ] Описание (truncated)
    - [ ] Дата создания
    - [ ] Действия: Редактировать, Удалить
  - [ ] Кнопка "Создать шаблон" → открывает модальное окно
  - [ ] Фильтры: категория, сложность (select)
  - [ ] Пагинация

- [ ] Модальное окно создания/редактирования (`components/admin/TaskTemplateModal.tsx`)
  - [ ] Dialog (shadcn/ui) с формой
  - [ ] Поля: title, description (textarea), category (select), difficulty (select)
  - [ ] Валидация через zod:
    - [ ] title: 1-200 символов
    - [ ] description: min 1 символ
    - [ ] category: 1-50 символов или select из предустановленных
    - [ ] difficulty: EASY | MEDIUM | HARD
  - [ ] Preview карточки задания (как будет видеть пользователь)
  - [ ] Mutations: `useCreateTemplate`, `useUpdateTemplate`
  - [ ] Toast уведомления

- [ ] Компонент удаления шаблона (`components/admin/DeleteTaskDialog.tsx`)
  - [ ] AlertDialog (shadcn/ui) для подтверждения
  - [ ] Mutation `useDeleteTemplate` с optimistic update
  - [ ] Toast уведомление

### Дашборд админа

- [ ] `app/(auth)/admin/page.tsx`
  - [ ] Карточки общей статистики (4 штуки):
    - [ ] Всего пользователей (useAdminUsers с подсчетом)
    - [ ] Активных пользователей за 7 дней (client-side подсчет)
    - [ ] Всего шаблонов заданий (useTaskTemplates с подсчетом)
    - [ ] Всего выполнено заданий (client-side подсчет через историю)
  - [ ] Секция: Последние регистрации (таблица 5 пользователей)
    - [ ] Сортировка по created_at DESC
    - [ ] Имя, email, дата регистрации
    - [ ] Link "Посмотреть всех" → `/admin/users`
  - [ ] Секция: Популярные категории заданий (таблица/список)
    - [ ] Группировка заданий по категориям
    - [ ] Отображение: категория, количество, badge
  - [ ] Секция: Quick Actions
    - [ ] Кнопки быстрого доступа (Создать шаблон, Посмотреть пользователей)

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

### shadcn/ui компоненты ✅

**ГОТОВО:** Установлены ВСЕ компоненты (50+ в `components/ui/`):
- [x] Button, Input, Textarea, Label, Form
- [x] Card, Table, Badge, Avatar
- [x] Dialog, Alert Dialog, Sheet, Drawer
- [x] Select, Dropdown Menu, Command, Popover
- [x] Tabs, Accordion, Collapsible
- [x] Alert, Sonner (Toast)
- [x] Skeleton, Progress, Spinner
- [x] Pagination, Breadcrumb
- [x] Calendar, Date Picker
- [x] Sidebar, Navigation Menu
- [x] Chart, Carousel
- [x] И другие...

### Утилиты

- [ ] `lib/utils/formatters.ts`
  - [ ] formatDate(date) - форматирование дат
  - [ ] formatProgress(completed, total) - процент выполнения
  - [ ] formatStreak(days) - форматирование серии

- [ ] `lib/utils/validators.ts`
  - [ ] Zod схемы для форм (login, register, task, etc.)

- [ ] `lib/hooks/use-auth.ts`
  - [ ] useLogin, useRegister, useLogout mutations
  - [ ] useCurrentUser query
  - [ ] Интеграция с auth store (zustand)

- [ ] `lib/hooks/use-tasks.ts`
  - [ ] useTodayTask query
  - [ ] useCompleteTask mutation
  - [ ] useTaskHistory query

- [ ] `lib/hooks/use-admin.ts`
  - [ ] useAdminUsers query
  - [ ] useAdminUserDetails query
  - [ ] useTaskTemplates query
  - [ ] useCreateTemplate, useUpdateTemplate, useDeleteTemplate mutations
  - [ ] useAssignTask mutation

---

## Приоритет 6: Дополнительные фичи

### Уведомления

- [ ] Настроить sonner Toaster (`app/layout.tsx`)
  - [ ] Toaster component в root layout
  - [ ] Theme integration (light/dark)

- [ ] Toast notifications для всех действий:
  - [ ] Успешный вход/регистрация
  - [ ] Выполнение задания (с именем задания)
  - [ ] Обновление профиля
  - [ ] Ошибки API (с понятным текстом)
  - [ ] CRUD операции в админке (создание/обновление/удаление)
  - [ ] Назначение заданий пользователям

### Responsive дизайн

- [ ] Адаптив для мобильных устройств
  - [ ] Мобильное меню (burger menu)
  - [ ] Адаптивная таблица (horizontal scroll или cards)
  - [ ] Touch-friendly кнопки

### Dark Mode (опционально)

- [ ] Переключатель темной/светлой темы
- [ ] Сохранение предпочтения в localStorage
- [ ] next-themes интеграция

**Примечания:**
- **Интернационализация (i18n)** - добавить позже, когда MVP готов
- **PWA (Progressive Web App)** - не требуется для MVP

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
// types/user.ts
export enum UserRole {
  USER = 'USER',
  ADMIN = 'ADMIN'
}

export interface User {
  id: string;
  name: string;
  email: string | null;
  telegram_id: number | null;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserProgress {
  total_tasks: number;
  completed_tasks: number;
  completion_rate: number; // 0-100
  streak_days: number;
}

// types/task.ts
export enum TaskDifficulty {
  EASY = 'EASY',
  MEDIUM = 'MEDIUM',
  HARD = 'HARD'
}

export enum AssignmentStatus {
  PENDING = 'PENDING',
  COMPLETED = 'COMPLETED'
}

export interface Task {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: TaskDifficulty;
  created_at: string;
}

export interface Assignment {
  id: string;
  user_id: string;
  task_id: string;
  assigned_date: string; // ISO date (YYYY-MM-DD)
  completed_at: string | null;
  status: AssignmentStatus;
  answer_text: string | null;
  created_at: string;
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

export interface RegisterResponse {
  user: User;
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// types/api.ts
export interface ApiError {
  detail: string;
  status?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}
```

---

## Приоритеты выполнения (рекомендуемый порядок)

### Sprint 1 (5-7 дней): Инфраструктура + Аутентификация ✅ ЗАВЕРШЕН
1. ✅ Инициализация проекта (Next.js 15 + TypeScript + Tailwind)
2. ✅ Установка зависимостей (TanStack Query, Axios, Zustand, shadcn/ui)
3. ✅ Настройка Axios клиента с interceptors
4. ✅ TanStack Query Provider + Devtools
5. ✅ Auth Store (Zustand) - только токены, с persist в localStorage
6. ✅ API методы для auth (register, login, refresh, logout)
7. ✅ Страницы login/register с формами (react-hook-form + zod)
8. ✅ Middleware для защиты роутов (проверка токенов)
9. ✅ Docker конфигурация (Dockerfile + docker-compose.yml + .dockerignore + standalone output)

### Sprint 2 (5-7 дней): Пользовательский кабинет ✅ ЗАВЕРШЕН
1. ✅ Layout (Header с навигацией, Footer)
2. ✅ Dashboard страница с карточками
3. ✅ Tasks страница (получение задания дня + выполнение)
4. ✅ History страница (список заданий + пагинация)
5. ✅ Stats страница (прогресс + статистика по категориям)
6. ✅ Profile страница (просмотр + редактирование)
7. ✅ Компоненты: TaskCard, CompleteTaskModal
8. ✅ Toast уведомления (sonner) - уже настроено в Sprint 1

### Sprint 3 (5-7 дней): Админ-панель ✅ ЗАВЕРШЕН
1. ✅ Middleware проверка роли admin
2. ✅ Admin Dashboard (общая статистика)
3. ✅ Список пользователей (таблица + фильтры)
4. ✅ Детали пользователя (профиль + история + назначение)
5. ✅ Управление шаблонами (CRUD)
6. ✅ Модальные окна: создание/редактирование/удаление шаблонов
7. ✅ API хуки для админки

### Sprint 4 (3-5 дней): Доработки + UX
1. Responsive дизайн (mobile/tablet)
2. Dark mode (опционально)
3. Улучшение UI/UX (loading states, error boundaries)
4. Accessibility (a11y)
5. SEO optimization (metadata)
6. Performance optimization

### Sprint 5 (2-3 дня): Deployment + Тестирование
1. Production build тестирование
2. Docker compose интеграция
3. Environment variables проверка
4. E2E тестирование (основные сценарии)
5. Bug fixes
6. Документация (README обновление)

**Общая оценка:** 3-4 недели на полную реализацию MVP

---

## Полезные ссылки

- [Next.js 15 Docs](https://nextjs.org/docs)
- [shadcn/ui](https://ui.shadcn.com/)
- [TanStack Query](https://tanstack.com/query/latest)
- [React Hook Form](https://react-hook-form.com/)
- [Zod](https://zod.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

---

**Создано:** 2025-10-05
**Статус:** Готово к разработке
**Предварительная оценка:** 4-5 недель на полную реализацию
