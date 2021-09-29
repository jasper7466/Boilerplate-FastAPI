import shutil
from typing import List

from fastapi import Depends
from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from passlib.hash import pbkdf2_sha256

from utils.append_updates import append_updates

from ..config import PROJECT_ROOT
from ..config import Settings
from ..config import get_settings
from ..database import Session
from ..database import get_session
from ..exeptions import EntityConflictError
from ..exeptions import EntityDoesNotExistError
from .models import AccountModel
from .schemas import AccountCreateSchema
from .schemas import AccountUpdateSchema


class AccountService:
    def __init__(
        self,
        session: Session = Depends(get_session),
        settings: Settings = Depends(get_settings)
    ):
        self.session = session
        self.settings = settings

    def create_account(self, account_create: AccountCreateSchema):
        account = AccountModel(
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

    def get_accounts(self) -> List[AccountModel]:
        accounts = self.session.execute(
            select(AccountModel)
        ).scalars().all()
        return accounts

    def get_account(self, account_id: int) -> AccountModel:
        return self._get_account(account_id)

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

    def _get_account(self, account_id: int) -> AccountModel:
        try:
            account = self.session.execute(
                select(AccountModel)
                .where(AccountModel.id == account_id)
            ).scalar_one()
        except NoResultFound:
            raise EntityDoesNotExistError from None
        return account
