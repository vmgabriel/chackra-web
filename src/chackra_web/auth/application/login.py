import pydantic

from chackra_web.auth.domain.models import auth as domain_auth
from chackra_web.auth.domain.models import repositories as auth_repositories
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.auth import auth_id as shared_auth_id

from chackra_web.auth.domain.services import get_by_email


class LoginDTO(pydantic.BaseModel):
    email: str
    password: str



class LoginCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    auth_repository: auth_repositories.AuthBaseRepository[domain_auth.AuthUser, shared_auth_id.AuthId]

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger

        self.auth_repository = dependencies.repository_store.build(
            auth_repositories.AuthBaseRepository[domain_auth.AuthUser, shared_auth_id.AuthId]
        )

    def execute(self, login_data: LoginDTO) -> domain_auth.AuthUser | None:
        current_user = get_by_email.get_by_email(email=login_data.email, auth_repository=self.auth_repository)
        if not current_user:
            return None
        if current_user.compare_password(to_compare_password=login_data.password):
            return current_user
        return None