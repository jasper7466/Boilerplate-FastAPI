# pylint: disable=C0413
# pylint: disable=W0611

"""Работа с базой данных"""

from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings


@event.listens_for(Engine, 'connect')
def enable_foreign_keys(dbapi_connection):
    """
    Функция включения проверки внешних ключей (для sqlite).
    Подписана на событие подключения к БД

    :param dbapi_connection: Подключение к БД
    :return: void
    """
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


engine = create_engine(
    settings.database_url,
    future=True,
    connect_args={'check_same_thread': False}
)

Session = sessionmaker(engine, future=True)


def get_session() -> Session:
    """
    Функция для создания сессии с последующим закрытием

    :return: Сессия
    """
    with Session() as session:
        yield session


Base = declarative_base()


from .accounts.models import AccountTable  # noqa
from .auth.models import RefreshTokenTable  # noqa
