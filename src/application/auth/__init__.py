"""Эндпоинт 'auth'"""

from fastapi import FastAPI

from .api import router


def attach_app(app: FastAPI):
    app.include_router(router)
