from fastapi import HTTPException
from fastapi import Depends
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel
from datetime import datetime
from datetime import timedelta

from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/accounts/login')


class AccountAuthModel(BaseModel):
    id: int
    email: str
    username: str


def create_token(account: AccountAuthModel, life_time: int) -> str:
    now = datetime.utcnow()
    return jwt.encode({
        'sub': str(account.id),
        'exp': now + timedelta(seconds=life_time),
        'iat': now,
        'nbf': now,
        'account': {
            'id': account.id,
            'email': account.email,
            'username': account.username,
        }
    }, settings.secret_key, 'HS256')


def get_current_account(
    token: str = Depends(oauth2_scheme),
) -> AccountAuthModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Unauthorized',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    token_data = jwt.decode(token, settings.secret_key, algorithms=['HS256'])

    if 'account' not in token_data:
        raise credentials_exception

    return AccountAuthModel(**token_data['account'])
