import pydantic
import datetime

from chackra_web.auth.domain.models import auth as domain_auth
from chackra_web.shared.domain.model.user import user_id as domain_user_id
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger

from chackra_web.shared.domain.model import dependencies as domain_dependencies


class AuthRegisterDTO(pydantic.BaseModel):
    email: str
    password: str
    user_id: domain_user_id.UserId


class AuthRegisterResponse(pydantic.BaseModel):
    id: str
    email: str
    user_id: domain_user_id.UserId
    auth_role: domain_auth.AuthRole
    created_at: datetime.datetime


class AuthRegisterService:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter

    def __init__(self, dependencies: domain_dependencies.ControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger

    def save(self, auth_register_dto: AuthRegisterDTO) -> AuthRegisterResponse:
        # Validations?

        new_auth = domain_auth.AuthUser.create(
            auth_user_data=domain_auth.BaseAuthUserDTO(
                email=auth_register_dto.email,
                password=auth_register_dto.password,
                user_id=auth_register_dto.user_id,
            )
        )

        # Persistence object?
        # Post Creation Object
        # Send Events?

        return AuthRegisterResponse(
            id=new_auth.id,
            email=new_auth.email,
            user_id=new_auth.user_id,
            auth_role=new_auth.auth_role,
            created_at=new_auth.created_at,
        )

