"""Приложение. Точка входа"""

import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from src.application.config import settings

from . import accounts
from . import auth


# Авто-создание директории со статикой, если её не существует
IS_STATIC_EXISTS = os.path.exists(settings.static_directory)
if not IS_STATIC_EXISTS:
    os.makedirs(settings.static_directory)

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie='session',
    max_age=100000,
)
app.mount(settings.static_url, StaticFiles(directory=settings.static_directory), name='static')
accounts.attach_app(app)
auth.attach_app(app)
