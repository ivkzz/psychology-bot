# Frontend Dockerfile для Next.js 15 приложения
FROM node:22-alpine AS base

# Устанавливаем зависимости только когда нужно
FROM base AS deps
# Проверяем https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine для понимания, почему libc6-compat может быть нужен
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Копируем файлы зависимостей
COPY package.json package-lock.json* ./
RUN npm ci

# Development stage
FROM base AS development
WORKDIR /app

# Копируем node_modules из deps
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Next.js собирает telemetry данные анонимно.
# Узнать больше: https://nextjs.org/telemetry
# Отключаем в development
ENV NEXT_TELEMETRY_DISABLED=1

# Expose порт для dev сервера
EXPOSE 3000

# Запускаем development сервер с hot reload
CMD ["npm", "run", "dev"]

# Builder stage - собираем production build
FROM base AS builder
WORKDIR /app

# Копируем node_modules из deps
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Next.js собирает telemetry данные анонимно.
# Отключаем в production build
ENV NEXT_TELEMETRY_DISABLED=1

# Сборка Next.js приложения
RUN npm run build

# Production stage
FROM base AS production
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Создаем непривилегированного пользователя
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Копируем только необходимые файлы для production
COPY --from=builder /app/public ./public

# Копируем standalone build (если включен output: 'standalone' в next.config.js)
# Если нет, то копируем .next целиком
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Запускаем Next.js production сервер
CMD ["node", "server.js"]
