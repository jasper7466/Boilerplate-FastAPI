from typing import List

from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from ..auth import AccountAuthModel, create_token
from ..auth import get_current_account
from ..exeptions import EntityConflictError
from ..exeptions import EntityDoesNotExistError
from .schemas import AccountSchema, TokensSchema, RefreshTokenSchema
from .schemas import AccountLoginSchema
from .schemas import AccountCreateSchema
from .schemas import AccountUpdateSchema
from .services import AccountService

router = APIRouter(
    prefix='/accounts'
)


@router.post('/login', response_model=TokensSchema)
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    account_service: AccountService = Depends(),
):
    account_login = AccountLoginSchema(
        username=credentials.username,
        password=credentials.password,
    )
    account = account_service.authenticate_account(account_login)
    return account_service.create_tokens(account)


@router.post('/refresh-token', response_model=TokensSchema)
def refresh_token(
    old_token: RefreshTokenSchema,
    account_service: AccountService = Depends(),
):
    try:
        account = account_service.get_account_by_refresh_token(old_token.token)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return account_service.create_tokens(account)


@router.post(
    '',
    response_model=AccountSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    account_create: AccountCreateSchema,
    service: AccountService = Depends(),
):
    try:
        account = service.create_account(account_create)
        return account
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT) from None


@router.get('', response_model=List[AccountSchema])
def get_accounts(
    current_account: AccountAuthModel = Depends(get_current_account),
    service: AccountService = Depends(),
):
    return service.get_accounts()


@router.get('/{account_id}', response_model=AccountSchema)
def get_account(
    account_id: int,
    service: AccountService = Depends(),
):
    try:
        return service.get_account(account_id)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None


@router.patch('/{account_id}', response_model=AccountSchema)
def edit_account(
    account_id: int,
    account_update: AccountUpdateSchema,
    service: AccountService = Depends(),
):
    try:
        account = service.update_account(account_id, account_update)
        return account
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None


@router.put('/{account_id}/avatar', response_model=AccountSchema)
def update_account_avatar(
    account_id: int,
    avatar: UploadFile = File(...),
    service: AccountService = Depends(),
):
    try:
        account = service.update_account_avatar(account_id, avatar)
        return account
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None
