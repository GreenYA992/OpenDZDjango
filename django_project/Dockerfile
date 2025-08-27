FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей (минимальные)
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Создаем папку для базы данных
RUN mkdir -p /app/db

# Порт для приложения
EXPOSE 8000

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]