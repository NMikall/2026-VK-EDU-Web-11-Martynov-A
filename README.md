## Локальный запуск

1. Скопируйте `.env.example` в `.env.local` командой `cp .env.example .env.local` (или `Copy-Item .env.example .env.local` на Win).
2. Запустите PostgreSQL и создайте базу и пользователя с правами на неё. В `.env.local` задайте случайный `SECRET_KEY` и заполните `DB_NAME`, `DB_USER` и `DB_PASSWORD`. Для PostgreSQL на этом же компьютере со стандартным портом укажите `DB_HOST=127.0.0.1` и `DB_PORT=5432`.
3. `python -m venv venv`
4. `source venv/bin/activate` (или `venv\Scripts\activate` на Win)
5. `pip install -r requirements.txt`
6. `python manage.py migrate`
7. `python manage.py runserver`

## Запуск через Docker

1. Скопируйте `.env.example` в `.env.docker` командой `cp .env.example .env.docker` (или `Copy-Item .env.example .env.docker` на Win).
2. В `.env.docker` задайте случайный `SECRET_KEY`, укажите `DB_HOST=db` и `DB_PORT=5432`. Заполните `POSTGRES_DB`, `POSTGRES_USER` и `POSTGRES_PASSWORD` и укажите те же значения в `DB_NAME`, `DB_USER` и `DB_PASSWORD` соответственно.
3. `docker compose up --build`
4. `docker compose exec web python manage.py migrate`.

## Создание суперпользователя

`python manage.py createsuperuser`

В Docker: `docker compose exec web python manage.py createsuperuser`

## Заполнение БД

`python manage.py fill_db 10001`

В Docker: `docker compose exec web python manage.py fill_db 10001`

## База данных

В качестве БД используется PostgreSQL.

## Авторизация и профиль
* Регистрация, вход и выход (`/signup/`, `/login/`, `/logout/`). После входа редирект на страницу из `?next=`.
* Страница `/profile/`: смена email, username, nickname и аватара. Аватары хранятся в `media/avatars/`.

## Вопросы и ответы
* Создание вопроса `/ask/` (до 3 тегов) и добавление ответа на странице вопроса доступны только авторизованным.
* После добавления ответа редирект на нужную страницу пагинации с прокруткой к ответу.
* Поиск по вопросам: `/search/?query=...`.

## AJAX
* Лайк и дизлайк вопросов и ответов без перезагрузки страницы. Один пользователь имеет один голос, клик по противоположной кнопке отменяет его.
* Отметка «лучший ответ» чекбоксом доступна только автору вопроса.