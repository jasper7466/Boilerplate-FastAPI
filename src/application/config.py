"""Конфигурация приложения"""

from pathlib import Path
from dynaconf import Dynaconf

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

PROJECT_ROOT = Path(__file__).parents[2]

# Псевдоним типа
Settings = Dynaconf

settings = Dynaconf(
    envvar_prefix="APPLICATION",
    settings_files=['settings.toml', '.secrets.toml'],
)


def get_settings() -> Dynaconf:
    """
    Функция для получения конфигурации

    :return: Настройки приложения
    """
    return settings
