"""Пользовательские исключения"""


class BaseServiceError(Exception):
    """Базовый класс ошибок"""


class ClientSideError(BaseServiceError):
    """Ошибки на стороне клиента"""


class ServerSideError(BaseServiceError):
    """Ошибки на стороне сервера"""


class EntityConflictError(ClientSideError):
    """Ошибка клиента: конфликт сущностей"""


class EntityDoesNotExistError(ClientSideError):
    """Ошибка клиента: сущность не существует"""
