# pylint: disable=R0801

"""Сервис 'accounts'"""

import shutil
from typing import List

from fastapi import Depends
from fastapi import UploadFile
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

from utils.append_updates import append_updates
from ..config import PROJECT_ROOT
from ..config import Settings
from ..config import get_settings
from ..database import Session
from ..database import get_session
from ..exceptions import EntityConflictError
from ..exceptions import EntityDoesNotExistError
from .models import AccountTable
from .schemas import AccountCreateSchema
from .schemas import AccountUpdateSchema


class AccountsService:
    """Сервис 'accounts'"""
    def __init__(
        self,
        session: Session = Depends(get_session),
        settings: Settings = Depends(get_settings),
    ):
        """
        Конструктор

        :param session: Сессия БД
        :param settings: Настройки приложения
        """
        self.session = session
        self.settings = settings

    def create_account(self, account_create: AccountCreateSchema) -> AccountTable:
        """
        Метод создания аккаунта

        :param account_create: Данные создаваемого аккаунта
        :return: Данные созданного аккаунта
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

    def get_accounts(self) -> List[AccountTable]:
        """
        Метод получения всех аккаунтов

        :return: Данные аккаунтов
        """
        accounts = self.session.execute(
            select(AccountTable)
        ).scalars().all()
        return accounts

    def get_account(self, account_id: int) -> AccountTable:
        """
        Метод получения аккаунта по id

        :param account_id: Идентификатор аккаунта
        :return: Данные аккаунта
        """
        return self._get_account(account_id)

    def update_account(self, account_id: int, account_update: AccountUpdateSchema):
        """
        Метод обновления аккаунта

        :param account_id: Идентификатор аккаунта
        :param account_update: Данные для обновления
        :return: Обновлённые данные аккаунта
        """
        account = self._get_account(account_id)
        append_updates(account, account_update)
        self.session.commit()

        return account

    def update_account_avatar(self, account_id: int, avatar: UploadFile):
        """
        Метод обновления аватара

        :param account_id: Идентификатор аккаунта
        :param avatar: Новое изображения аватара
        :return: Обновлённые данные аккаунта
        """
        account = self._get_account(account_id)

        filepath = PROJECT_ROOT / self.settings.static_directory / avatar.filename
        with filepath.open(mode='wb') as file:
            shutil.copyfileobj(avatar.file, file)
        file_url = f'{self.settings.static_url}/{avatar.filename}'

        account.avatar = file_url

        self.session.commit()
        return account

    def _get_account(self, account_id: int) -> AccountTable:
        """
        Приватный метод получения аккаунта по id

        :param account_id: Идентификатор аккаунта
        :return: Данные аккаунта
        """
        try:
            account = self.session.execute(
                select(AccountTable)
                .where(AccountTable.id == account_id)
            ).scalar_one()
            return account
        except NoResultFound:
            raise EntityDoesNotExistError from None
