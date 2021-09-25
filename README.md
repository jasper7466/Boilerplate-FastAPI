> &#10060; &dArr; &dArr; &dArr; BOILERPLATE DESCRIPTION. REMOVE BEFORE FLIGHT &dArr; &dArr; &dArr; &#10060;

# Boilerplate-FastAPI

# Manual creation log

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
- Создана директория src
- Создан пакет `src/application`
- Настроено минимальное приложение в src/application/app.py
- В настройках Run/Debug конфигурации среды разработки необходимо создать новую с параметрами:
  - Target to run - Module name: (указать название пакета приложения, в данном случае - application)
  - Python interpreter: (выбрать из локального venv)
  - Working directory: (указать корень проекта)


</details>

> &#10060; &uArr; &uArr; &uArr; BOILERPLATE DESCRIPTION. REMOVE BEFORE FLIGHT &uArr; &uArr; &uArr; &#10060;

# YourProject:Name

Generated from [jasper7466/Boilerplate-FastAPI](https://github.com/jasper7466/Boilerplate-FastAPI)