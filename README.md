> &#10060; &dArr; &dArr; &dArr; BOILERPLATE DESCRIPTION. REMOVE BEFORE FLIGHT &dArr; &dArr; &dArr; &#10060;

# Boilerplate-FastAPI

## Назначение

Шаблонный репозиторий для генерации проектов HTTP API сервисов на базе фреймворка FastAPI

## Что внутри

- Менеджмент пакетов: Poetry
- HTTP API фреймворк: FastAPI

## Лог ручной инициализации

<details>
  <summary>Click!</summary>

  ### Менеджер пакетов Poetry
  
  - Установка пакета `Poetry` (если не установлен)
    > pip install poetry
  - Poetry. Локальная конфигурация: создавать venv в корне проекта
    > poetry config virtualenvs.in-project true --local
  - Poetry. Инициализация
    > poetry init
  - Poetry. Создание venv
    > poetry env use python3.9
  - Poetry. Активация venv
    > poetry shell
  - В среде разработки для проекта необходимо выбрать интерпретатор из локального venv
  
  ### Фреймворк FastAPI
  
  - Установка пакета `FastAPI`
    > poetry add fastapi
  - Установка пакета `Uvicorn` (ASGI-сервер)
    > poetry add uvicorn
  - Установка пакета `python-multipart`
    > poetry add python-multipart
  - Создана директория src
  - Создан пакет `src/application`
  - Настроено минимальное приложение в src/application/app.py
  - В настройках Run/Debug конфигурации среды разработки необходимо создать новую с параметрами:
    - Target to run - Module name: (указать название пакета приложения, в данном случае - application)
    - Python interpreter: (выбрать из локального venv)
    - Working directory: (указать корень проекта)
  
  ### Работа с конфигурацией приложения

  - Установка пакета `dynaconf`
    > poetry add dynaconf
  - Инициализация конфига
    > dynaconf init
  - Конфигурационный файл config.py следует перенести в пакет (application)
  - Параметр envvar_prefix можно заменить на свой (например, APPLICATION)

  ### Работа с БД

  - Установка пакета `sqlalchemy`
    > poetry add sqlalchemy
  - Установка пакета `aiofiles`
    > poetry add aiofiles
  - Установка пакета `alembic`
    > poetry add alembic
  - Инициализация alembic
    > alembic init
  - Конфигурация settings.toml
    - `database_url = "sqlite:///database.sqlite"`
  - Конфигурация в alembic.ini
    - `prepend_sys_path = src`
    - `file_template = %%(year)d-%%(month).2d-%%(day).2d_%%(hour).2d:%%(minute).2d:%%(second).2d_%%(rev)s`
    - `# sqlalchemy.url = driver://user:pass@localhost/dbname` - закомментировать
  - Конфигурация в alembic/env.py
    - `target_metadata = Base.metadata`
    - `config.set_main_option('sqlalchemy.url', settings.database_url)`
  - Создание миграции
    - `alembic revision --autogenerate -m "Create 'accounts' table"`
  - Применение миграции
    - `alembic upgrade head`

  ### Реализация ручек аккаунта
  - Установка пакета `passlib`
    > poetry add passlib
  - Установка пакета `python-multipart`
    > poetry add python-multipart
  - config.py:
    - `PROJECT_ROOT = Path(__file__).parents[2]`
  - Создана модель AccountModel в models.py
  - Добавлены ручки в app.py
</details>

> &#10060; &uArr; &uArr; &uArr; BOILERPLATE DESCRIPTION. REMOVE BEFORE FLIGHT &uArr; &uArr; &uArr; &#10060;

# YourProject:Name

Generated from [jasper7466/Boilerplate-FastAPI](https://github.com/jasper7466/Boilerplate-FastAPI)