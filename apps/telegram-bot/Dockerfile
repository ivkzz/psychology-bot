# Telegram Bot Dockerfile
FROM python:3.11-slim as base

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Development stage
FROM base as development
RUN pip install --no-cache-dir debugpy pytest pytest-asyncio
COPY . .
ENV PYTHONPATH=/app
CMD ["python", "-u", "bot/main.py"]

# Production stage
FROM base as production
COPY . .
# Создаем непривилегированного пользователя
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser
ENV PYTHONPATH=/app
CMD ["python", "-u", "bot/main.py"]
