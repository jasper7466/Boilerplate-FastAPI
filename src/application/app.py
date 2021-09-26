import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import settings
from .accounts import api as accounts_api


# Авто-создание директории со статикой, если её не существует
is_static_exists = os.path.exists(settings.static_directory)
if not is_static_exists:
    os.makedirs(settings.static_directory)

app = FastAPI()
app.mount(settings.static_url, StaticFiles(directory=settings.static_directory), name='static')
accounts_api.initialize_app(app)
