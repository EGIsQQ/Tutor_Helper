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

## Структура

```text
app/
├── backend/
│   └── ...
├── models/
│   ├── student.py
│   └── lessons_reports.py
├── routers/
│   ├── students.py
│   └── lesson_reports.py
├── templates/
│   ├── student_reports.html
│   ├── edit_report.html
│   └── ...
├── schemas.py
└── main.py
```

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

```bash
uvicorn app.main:app --reload
```

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:8000
```

## Статус проекта

Проект находится в разработке. В дальнейшем планируется добавить авторизацию пользователей, AI-помощника для анализа истории занятий ученика и расписание занятий.

