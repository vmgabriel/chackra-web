from chackra_web.shared.domain.model.exceptions import exception as shared_exception

import enum


class ExceptionCodeError(enum.StrEnum):
    AUTH_HAS_ALREADY_REGISTERED = "auth_has_already_registered"


class AuthExistsException(shared_exception.SystemException):
    def __init__(self) -> None:
        message = shared_exception.ExceptionMessage(
            title="Registro de Auth ya realizado",
            description="El registro de Auth ya esta configurado, quizas, deba revisar como esta integrado el sistema",
            code=str(ExceptionCodeError.AUTH_HAS_ALREADY_REGISTERED.value),
        )
        super().__init__(message=message, status_code=401)