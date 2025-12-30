import pydantic

from chackra_web.shared.domain.model.user import user_id as domain_user_id
from chackra_web.shared.domain.model.auth import auth_id as domain_auth_id, enums as auth_enums
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies

from chackra_web.auth.domain.models import repositories as auth_repositories, auth as domain_auth

from chackra_web.auth.domain.services import get_by_user_id as auth_get_by_user_id


class ChangeRoleDTO(pydantic.BaseModel):
    user_id: domain_user_id.UserId
    role: auth_enums.AuthRole


class ChangeRoleCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    auth_repository: auth_repositories.AuthBaseRepository[domain_auth.AuthUser, domain_auth_id.AuthId]

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger

        self.auth_repository = dependencies.repository_store.build(
            auth_repositories.AuthBaseRepository[domain_auth.AuthUser, domain_auth_id.AuthId]
        )

    def execute(self, change_role_dto: ChangeRoleDTO) -> None:
        auth_entity = auth_get_by_user_id.get_by_user_id(
            user_id=change_role_dto.user_id,
            auth_repository=self.auth_repository
        )
        if not auth_entity:
            self.logger.error(f"Auth entity not found for user_id: {change_role_dto.user_id}")
            return None

        auth_id = auth_entity.id
        self.auth_repository.change_role(id=auth_id, role=change_role_dto.role)
        return None

