from chackra_web.shared.domain.model.exceptions import exception as shared_exception

import enum

class ExceptionCodeError(enum.StrEnum):
    USER_HAS_ALREADY_REGISTERED = "user_has_already_registered"


class UserExistsException(shared_exception.SystemException):
    def __init__(self) -> None:
        message = shared_exception.ExceptionMessage(
            title="Usuario ya registrado",
            description="El usuario ya existe, no se va a registrar",
            code=str(ExceptionCodeError.USER_HAS_ALREADY_REGISTERED.value),
        )
        super().__init__(message=message, status_code=401)
