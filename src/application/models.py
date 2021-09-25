from typing import Optional
from pydantic import BaseModel


class AccountModel(BaseModel):
    id: int
    email: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[str]

    class Config:
        orm_mode = True
