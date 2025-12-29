import pydantic
import datetime

from chackra_web.auth.domain.models import auth as domain_auth
from chackra_web.auth.domain.models import repositories as auth_repositories
from chackra_web.auth.domain.models import exceptions as auth_exceptions

from chackra_web.shared.domain.model.user import user_id as domain_user_id
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.auth import auth_id as shared_auth_id, enums as shared_auth_enums


class AuthRegisterDTO(pydantic.BaseModel):
    email: str
    password: str
    user_id: domain_user_id.UserId


class AuthRegisterResponse(pydantic.BaseModel):
    id: shared_auth_id.AuthId
    email: str
    user_id: domain_user_id.UserId
    auth_role: shared_auth_enums.AuthRole
    created_at: datetime.datetime


class AuthRegisterService:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    auth_repository: auth_repositories.AuthBaseRepository[domain_auth.AuthUser, shared_auth_id.AuthId]

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger

        self.auth_repository = dependencies.repository_store.build(
            auth_repositories.AuthBaseRepository[domain_auth.AuthUser, shared_auth_id.AuthId]
        )

    def save(self, auth_register_dto: AuthRegisterDTO) -> AuthRegisterResponse:
        new_auth = domain_auth.AuthUser.create(
            auth_user_data=domain_auth.BaseAuthUserDTO(
                email=auth_register_dto.email,
                password=auth_register_dto.password,
                user_id=auth_register_dto.user_id,
            )
        )

        self.auth_repository.find_by_email(email=new_auth.email)

        if self.auth_repository.find_by_email(email=new_auth.email):
            raise auth_exceptions.AuthExistsException()

        created = self.auth_repository.create(entity=new_auth)

        return AuthRegisterResponse(
            id=created.id,
            email=created.email,
            user_id=created.user_id,
            auth_role=created.auth_role,
            created_at=created.created_at,
        )

