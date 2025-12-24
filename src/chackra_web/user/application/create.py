import pydantic

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.user import user_id as shared_user_id

from chackra_web.user.domain.models import user as domain_user, repositories as user_repositories
from chackra_web.user.domain.models import exceptions as user_exceptions


class CreateUserDTO(pydantic.BaseModel):
    username: str
    name: str
    last_name: str
    email: str


class CreateUserCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    user_repository:  user_repositories.UserBaseRepository[domain_user.User, shared_user_id.UserId]

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger

        self.user_repository = dependencies.repository_store.build(
            user_repositories.UserBaseRepository[domain_user.User, shared_user_id.UserId]
        )

    def execute(self, create_user_dto: CreateUserDTO) -> domain_user.User:
        user_created = domain_user.User.create(
            user_data=domain_user.UserCreateDTO(
                username=create_user_dto.username,
                name=create_user_dto.name,
                last_name=create_user_dto.last_name,
                email=create_user_dto.email
            )
        )

        user_exists = self.user_repository.find_unique_by_username_and_email(
            username=create_user_dto.username,
            email=create_user_dto.email
        )

        if user_exists:
            raise user_exceptions.UserExistsException()

        return self.user_repository.create(entity=user_created)