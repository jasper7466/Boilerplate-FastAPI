"""Модели данных эндпоинта 'auth'"""

from pydantic import BaseModel


class AuthAccountSchema(BaseModel):
    """Модель аккаунта"""
    id: int
    email: str
    username: str


class TokensPairSchema(BaseModel):
    """Модель токена"""
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
