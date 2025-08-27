# Employee Management System

## Локальный запуск

# 1. Установите зависимости:
```bash

pip install -r requirements.txt
```

# 2. Применение миграции:
```bash
python manage.py migrate
```

# 3. Запуск сервера:
```bash
python manage.py runserver
```

## Запуск через Docker

# 4. Сборка и запуск контейнеров:
```bash
docker-compose up --build
```

# 5. Применение миграции в контейнере:
```bash
docker-compose exec web python manage.py migrate
```

# 6. Создание суперпользователя:
```bash
docker-compose exec web python manage.py migrate
```
