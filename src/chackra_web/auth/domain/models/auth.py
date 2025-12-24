import pydantic
import enum
import datetime
import uuid

from chackra_web.shared.domain.model.user import user_id as domain_user_id
from chackra_web.shared.domain.model.auth import auth_id as domain_auth_id

class AuthRole(enum.StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"


class BaseAuthUserDTO(pydantic.BaseModel):
    email: str
    password: str
    user_id: domain_user_id.UserId
    auth_role: AuthRole = AuthRole.USER


class AuthUser(pydantic.BaseModel):
    id: domain_auth_id.AuthId
    email: str
    password: str
    user_id: domain_user_id.UserId
    auth_role: AuthRole = AuthRole.USER
    active: bool = True

    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()
    deleted_at: datetime.datetime | None = None

    @staticmethod
    def create(auth_user_data: BaseAuthUserDTO) -> "AuthUser":
        return AuthUser(
            id=domain_auth_id.AuthId(value=str(uuid.uuid4())),
            email=auth_user_data.email,
            password=auth_user_data.password,
            user_id=auth_user_data.user_id,
            auth_role=auth_user_data.auth_role,
        )
