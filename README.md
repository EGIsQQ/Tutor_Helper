# Tutor Helper

Веб-приложение для ведения дневника репетитора.

Позволяет хранить информацию об учениках и вести отчёты по проведённым занятиям.

## Возможности

* добавление и просмотр учеников;
* просмотр истории занятий конкретного ученика;
* создание отчётов после занятий;
* редактирование отчётов;
* удаление ученика;
* хранение темы урока, прогресса, сложностей, домашнего задания и плана следующего занятия.

## Стек

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* Jinja2
* HTML / CSS / JavaScript
* asyncpg


## Запуск

Клонировать репозиторий:

```bash
git clone <repository-url>
cd tutor_helper
```

Создать виртуальное окружение:

```bash
python -m venv .venv
```

Активировать его:

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

Установить зависимости:

```bash
pip install -r requirements.txt
```

Настроить подключение к PostgreSQL и запустить приложение:

Добавляем в корневую папку .env и заполняем его своими данными: 

```.env
SECRET_KEY=secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=database_url
REDIS_HOST=localhost
REDIS_PORT=6379
CELERY_BROKER_URL=celery_broker_url
EMAIL_USER=почта_с_которой_будет_приходить_код_авторизации
EMAIL_APP_PASSWORD=smtp_email_pass
SMTP_PORT=465
SMTP_HOST=smtp_host
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=postgres_db
```

Создаем в корневой папке docker-compose.yaml
Добавляем в файл данный код: 

```docker-compose.yaml
services:
  db:
    image: postgres:16.2
    restart: always
    shm_size: 128mb
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "8080:5432" 

  cache: 
    image: redis:7.2.4-alpine
    restart: always
    ports:
      - "6379:6379"
```

Собираем контейнер: 

```bash
docker compose up -d --build
```

Запускаем celery:

 Windows:
```bash
celery -A worker.celery worker --loglevel=info --pool=solo
```

Запускаем локально проект

```bash
uvicorn app.main:app --reload
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:8000
```

## Статус проекта

Проект находится в разработке. В дальнейшем планируется добавить AI-помощника для анализа истории занятий ученика, расписание занятий и админ панель для учителя.

