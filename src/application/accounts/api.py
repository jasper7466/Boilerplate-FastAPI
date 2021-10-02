# pylint: disable=W0613

"""Ручки аккаунта"""

from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status

from .schemas import AccountSchema
from .schemas import AccountCreateSchema
from .schemas import AccountUpdateSchema
from .services import AccountsService
from ..auth.dependencies import get_current_account
from ..auth.schemas import AuthAccountSchema
from ..exceptions import EntityConflictError
from ..exceptions import EntityDoesNotExistError

ENDPOINT_TAG = 'accounts'

router = APIRouter(
    prefix=f'/{ENDPOINT_TAG}',
)


@router.post(
    '',
    response_model=AccountSchema,
    status_code=status.HTTP_201_CREATED,
    tags=[ENDPOINT_TAG],
)
def create_account(
    account_create: AccountCreateSchema,
    service: AccountsService = Depends(),
):
    """
    Ручка создания аккаунта

    :param account_create: Параметры аккаунта.
    :param service: Сервис.
    :return: Данные созданного аккаунта.
    """
    try:
        account = service.create_account(account_create)
        return account
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT) from None


@router.get('', response_model=List[AccountSchema], tags=[ENDPOINT_TAG])
def get_accounts(
    current_account: AuthAccountSchema = Depends(get_current_account),
    service: AccountsService = Depends(),
):
    """
    Ручка получения всех аккаунтов

    :param current_account: Данные текущего аккаунта
    :param service: Сервис
    :return: Аккаунты
    """
    return service.get_accounts()


@router.get('/{account_id}', response_model=AccountSchema, tags=[ENDPOINT_TAG])
def get_account(
    account_id: int,
    current_account: AuthAccountSchema = Depends(get_current_account),
    service: AccountsService = Depends(),
):
    """
    Ручка получения аккаунта по id

    :param account_id: Идентификатор аккаунта
    :param current_account: Данные текущего аккаунта
    :param service: Сервис
    :return: Данные запрашиваемого аккаунта
    """
    try:
        return service.get_account(account_id)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None


@router.patch('/{account_id}', response_model=AccountSchema, tags=[ENDPOINT_TAG])
def edit_account(
    account_id: int,
    account_update: AccountUpdateSchema,
    current_account: AuthAccountSchema = Depends(get_current_account),
    service: AccountsService = Depends(),
):
    """
    Ручка редактирования аккаунта

    :param account_id: Идентификатор аккаунта
    :param account_update: Данные для обновления аккаунта
    :param current_account: Данные текущего аккаунта
    :param service: Сервис
    :return: Обновлённые данные аккаунта
    """
    try:
        account = service.update_account(account_id, account_update)
        return account
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None


@router.put('/{account_id}/avatar', response_model=AccountSchema, tags=[ENDPOINT_TAG])
def update_account_avatar(
    account_id: int,
    avatar: UploadFile = File(...),
    current_account: AuthAccountSchema = Depends(get_current_account),
    service: AccountsService = Depends(),
):
    """
    Ручка обновления аватара

    :param account_id: Идентификатор аккаунта
    :param avatar: Новое изображение аватара
    :param current_account: Данные текущего аккаунта
    :param service: Сервис
    :return: Обновлённые данные аккаунта
    """
    try:
        account = service.update_account_avatar(account_id, avatar)
        return account
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None
