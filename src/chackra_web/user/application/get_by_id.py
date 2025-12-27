import pydantic

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.user import user_id as shared_user_id

from chackra_web.user.domain.models import user as domain_user, repositories as user_repositories
from chackra_web.user.domain.services import get_by_id as user_get_by_id


class GetByIDUserDTO(pydantic.BaseModel):
    user_id: str

    def to_user_id(self) -> shared_user_id.UserId:
        return shared_user_id.UserId(value=self.user_id)


class GetByIdUserCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    user_repository:  user_repositories.UserBaseRepository[domain_user.User, shared_user_id.UserId]

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger

        self.user_repository = dependencies.repository_store.build(
            user_repositories.UserBaseRepository[domain_user.User, shared_user_id.UserId]
        )

    def execute(self, get_by_id_user_dto: GetByIDUserDTO) -> domain_user.User | None:
        return user_get_by_id.get_by_id(user_id=get_by_id_user_dto.to_user_id(), user_repository=self.user_repository)