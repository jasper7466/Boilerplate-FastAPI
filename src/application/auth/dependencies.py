# pylint: disable=C0114

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose import jwt
from pydantic import ValidationError

from .schemas import AuthAccountSchema
from ..config import Settings
from ..config import get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/accounts/login')


def get_current_account(
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
) -> AuthAccountSchema:
    """
    Функция получения аккаунта по токену

    :param token: Токен
    :param settings: Настройки приложения
    :return: AuthAccountSchema
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Unauthorized user',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        token_data = jwt.decode(token, settings.secret_key, algorithms=['HS256'])
    except JWTError:
        raise credentials_exception from None

    try:
        return AuthAccountSchema(**token_data.get('account', {}))
    except ValidationError:
        raise credentials_exception from None
