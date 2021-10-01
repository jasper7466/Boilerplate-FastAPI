from pydantic import BaseModel


class AuthAccountSchema(BaseModel):
    id: int
    email: str
    username: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
