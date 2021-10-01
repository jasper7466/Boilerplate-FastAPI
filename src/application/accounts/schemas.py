from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel


class AccountSchema(BaseModel):
    id: int
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[str]

    class Config:
        orm_mode = True


class AccountCreateSchema(BaseModel):
    email: str
    username: str
    password: str


class AccountUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class AccountLoginSchema(BaseModel):
    username: str
    password: str


class RefreshTokenSchema(BaseModel):
    token: str


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
