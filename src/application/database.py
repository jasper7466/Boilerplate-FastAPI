from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings


# Включение проверки внешних ключей (для sqlite)
@event.listens_for(Engine, 'connect')
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


engine = create_engine(
    settings.database_url,
    future=True,
    connect_args={'check_same_thread': False}
)


Session = sessionmaker(engine, future=True)
Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    avatar = Column(String)
