"""Ручки авторизации"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import TokensPairSchema
from .services import AuthService
from ..exceptions import EntityDoesNotExistError

ENDPOINT_TAG = 'auth'

router = APIRouter(
    prefix=f'/{ENDPOINT_TAG}',
)


@router.post('/login', response_model=TokensPairSchema, tags=[ENDPOINT_TAG])
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    """
    Ручка авторизации

    :param credentials: Реквизиты для входа
    :param auth_service: Сервис авторизации
    :return: TokensPairSchema
    """
    try:
        return auth_service.authenticate(credentials.username, credentials.password)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED) from None


@router.post('/token', tags=[ENDPOINT_TAG])
def token(
    refresh_token: str = Form(...),
    auth_service: AuthService = Depends(),
):
    """
    Ручка получения нового токена

    :param refresh_token: Токен для обновления
    :param auth_service: Сервис авторизации
    :return: TokensPairSchema
    """
    try:
        return auth_service.refresh_token_pair(refresh_token)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED) from None
