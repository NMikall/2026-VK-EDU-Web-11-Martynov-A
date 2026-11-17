## Локальный запуск

1. `python -m venv venv`
2. `source venv/bin/activate` (или `venv\Scripts\activate` на Win)
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py runserver`

## Запуск через Docker

1. `docker compose up --build`
2. `docker compose exec web python manage.py migrate`

## Создание суперпользователя

`python manage.py createsuperuser`

В Docker: `docker compose exec web python manage.py createsuperuser`

## Заполнение БД

`python manage.py fill_db 10001`

В Docker: `docker compose exec web python manage.py fill_db 10001`

## База данных

В качестве БД используется PostgreSQL.