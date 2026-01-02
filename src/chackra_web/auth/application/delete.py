import pydantic

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.user import user_id as shared_user_id
from chackra_web.auth.domain.models import repositories as auth_repositories
from chackra_web.auth.domain.models import auth as domain_auth
from chackra_web.shared.domain.model.auth import auth_id as shared_auth_id

from chackra_web.auth.domain.services import get_by_user_id as auth_get_by_user_id


class DeleteUserDTO(pydantic.BaseModel):
    user_id: shared_user_id.UserId


class DeleteAuthCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    auth_repository: auth_repositories.AuthBaseRepository[domain_auth.AuthUser, shared_auth_id.AuthId]

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger

        self.auth_repository = dependencies.repository_store.build(
            auth_repositories.AuthBaseRepository[domain_auth.AuthUser, shared_auth_id.AuthId]
        )

    def execute(self, delete_user_dto: DeleteUserDTO) -> None:
        auth_entity = auth_get_by_user_id.get_by_user_id(
            user_id=delete_user_dto.user_id,
            auth_repository=self.auth_repository
        )
        if not auth_entity:
            return None

        return self.auth_repository.delete(id=auth_entity.id)
