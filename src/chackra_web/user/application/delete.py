import pydantic

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.user import user_id as shared_user_id

from chackra_web.user.domain.models import user as domain_user, repositories as user_repositories


class DeleteUserDTO(pydantic.BaseModel):
    user_id: shared_user_id.UserId


class DeleteUserCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    user_repository:  user_repositories.UserBaseRepository[domain_user.User, shared_user_id.UserId]

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger

        self.user_repository = dependencies.repository_store.build(
            user_repositories.UserBaseRepository[domain_user.User, shared_user_id.UserId]
        )

    def execute(self, delete_user_dto: DeleteUserDTO) -> None:
        return self.user_repository.delete(delete_user_dto.user_id)