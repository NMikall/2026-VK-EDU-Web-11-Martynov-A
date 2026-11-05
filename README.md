# HW-2 - Обработка HTTP запросов

## Локальный запуск

1. `python -m venv .venv`
2. `source .venv/bin/activate` (или `.venv\Scripts\activate` на Windows)
3. `pip install -r requirements.txt`
4. `cp .env.example .env`
5. `python manage.py runserver`

Сайт откроется на http://127.0.0.1:8000

## Запуск через Docker

1. `cp .env.example .env`
2. `docker compose up --build`

Сайт откроется на http://localhost:8000
