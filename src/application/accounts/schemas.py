# pylint: disable=C0114
# pylint: disable=C0115
"""Модели данных эндпоинта 'accounts'"""

from typing import Optional

from pydantic import BaseModel


class AccountSchema(BaseModel):
    """Модель аккаунта"""
    id: int
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[str]

    class Config:
        orm_mode = True


class AccountCreateSchema(BaseModel):
    """Модель данных для создания аккаунта"""
    email: str
    username: str
    password: str


class AccountUpdateSchema(BaseModel):
    """Модель данных для обновления аккаунта"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
