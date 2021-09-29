class BaseServiceError(Exception):
    pass


class ClientSideError(BaseServiceError):
    pass


class ServerSideError(BaseServiceError):
    pass


class EntityConflictError(ClientSideError):
    pass


class EntityDoesNotExistError(ClientSideError):
    pass