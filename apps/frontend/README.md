# Psychology Bot - Frontend

Frontend приложение на Next.js 15 для Psychology Bot.

## Технологии

- **Next.js 15** - React фреймворк с App Router
- **TypeScript** - типизация
- **Tailwind CSS** - стилизация
- **shadcn/ui** - UI компоненты
- **TanStack Query** - управление server state
- **Zustand** - управление client state (auth токены)
- **React Hook Form + Zod** - формы и валидация
- **Axios** - HTTP клиент

## Запуск через Docker (рекомендуется)

### Development режим

Из корневой директории проекта:

```bash
# Запустить все сервисы (backend, frontend, postgres, telegram-bot)
docker compose -f docker-compose.dev.yml up

# Или только frontend (если backend уже запущен)
docker compose -f docker-compose.dev.yml up frontend
```

Frontend будет доступен на [http://localhost:3000](http://localhost:3000)

### Production режим

```bash
# Собрать и запустить production build
docker compose up frontend

# Или собрать образ отдельно
docker build -t psychology-bot-frontend --target production .
docker run -p 3000:3000 psychology-bot-frontend
```

## Локальный запуск (без Docker)

### Установка зависимостей

```bash
npm install
```

### Настройка окружения

Создайте `.env.local` файл (уже существует):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Запуск development сервера

```bash
npm run dev
```

Откройте [http://localhost:3000](http://localhost:3000) в браузере.

### Production build

```bash
npm run build
npm run start
```

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
