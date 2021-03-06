"""Модели таблиц эндпоинта 'account'"""

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from ..database import Base


class AccountTable(Base):
    """Таблица аккаунтов"""
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    avatar = Column(String)
