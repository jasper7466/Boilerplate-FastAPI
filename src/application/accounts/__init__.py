"""Эндпоинт 'accounts'"""

from fastapi import FastAPI

from .api import router


def attach_app(app: FastAPI):
    """
    Функция подключения роута к приложению

    :param app: FastAPI-приложение
    :return: void
    """
    app.include_router(router)
