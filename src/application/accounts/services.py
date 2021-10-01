"""
Сервис "accounts"
"""

import shutil
from typing import List

from fastapi import Depends
from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from passlib.hash import pbkdf2_sha256

from utils.append_updates import append_updates

from ..auth import create_token
from ..config import PROJECT_ROOT
from ..config import Settings
from ..config import get_settings
from ..database import Session
from ..database import get_session
from ..exeptions import EntityConflictError
from ..exeptions import EntityDoesNotExistError
from .models import AccountTable
from .models import RefreshTokenTable
from .schemas import AccountCreateSchema
from .schemas import AccountLoginSchema
from .schemas import TokensSchema
from .schemas import AccountUpdateSchema


class AccountService:
    """
    Сервис "accounts"
    """
    def __init__(
        self,
        session: Session = Depends(get_session),
        settings: Settings = Depends(get_settings)
    ):
        """
        Конструктор
        :param session: Подключение к БД
        :param settings: Глобальная конфигурация приложения
        """
        self.session = session
        self.settings = settings

    def create_account(self, account_create: AccountCreateSchema):
        """
        Метод создания нового аккаунта
        :param account_create: Параметры создаваемого аккаунта
        :return: Параметры созданного аккаунта
        """
        account = AccountTable(
            email=account_create.email,
            username=account_create.username,
            password=pbkdf2_sha256.hash(account_create.password),
        )
        self.session.add(account)
        try:
            self.session.commit()
            return account
        except IntegrityError:
            raise EntityConflictError from None

    def authenticate_account(self, account_login: AccountLoginSchema) -> AccountTable:
        """
        Метод аутентификации
        :param account_login:
        :return:
        """
        try:
            account = self.session.execute(
                select(AccountTable)
                .where(AccountTable.username == account_login.username)
            ).scalar_one()
        except NoResultFound:
            raise EntityDoesNotExistError from None
        if not pbkdf2_sha256.verify(account_login.password, account.password):
            raise EntityDoesNotExistError from None
        return account

    def create_tokens(self, account: AccountTable) -> TokensSchema:
        access_token = create_token(account, life_time=self.settings.jwt_access_lifetime)
        refresh_token = create_token(account, life_time=self.settings.jwt_refresh_lifetime)

        try:
            account_token = self.session.execute(
                select(RefreshTokenTable)
                .where(RefreshTokenTable.account_id == account.id)
            ).scalar_one()
            account_token.token = refresh_token
        except NoResultFound:
            self.session.add(RefreshTokenTable(
                account_id=account.id,
                token=refresh_token,
            ))

        self.session.commit()
        return TokensSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type='bearer',
        )

    def get_accounts(self) -> List[AccountTable]:
        accounts = self.session.execute(
            select(AccountTable)
        ).scalars().all()
        return accounts

    def get_account(self, account_id: int) -> AccountTable:
        return self._get_account(account_id)

    def get_account_by_username(self, username: str) -> AccountTable:
        try:
            account = self.session.execute(
                select(AccountTable)
                .where(AccountTable.username == username)
            ).scalar_one()
        except NoResultFound:
            raise EntityDoesNotExistError from None
        return account

    def get_account_by_refresh_token(self, token: str) -> AccountTable:
        try:
            account = self.session.execute(
                select(AccountTable)
                .join_from(AccountTable, RefreshTokenTable)
                .where(RefreshTokenTable.token == token)
            ).scalar_one()
            return account
        except NoResultFound:
            raise EntityDoesNotExistError from None

    def update_account(self, account_id: int, account_update: AccountUpdateSchema):
        account = self._get_account(account_id)
        account = append_updates(account, account_update)

        self.session.commit()
        return account

    def update_account_avatar(self, account_id: int, avatar: UploadFile):
        account = self._get_account(account_id)

        filepath = PROJECT_ROOT / self.settings.static_directory / avatar.filename
        with filepath.open(mode='wb') as f:
            shutil.copyfileobj(avatar.file, f)
        file_url = f'{self.settings.static_url}/{avatar.filename}'
        account.avatar = file_url

        self.session.commit()
        return account

    def _get_account(self, account_id: int) -> AccountTable:
        try:
            account = self.session.execute(
                select(AccountTable)
                .where(AccountTable.id == account_id)
            ).scalar_one()
        except NoResultFound:
            raise EntityDoesNotExistError from None
        return account
