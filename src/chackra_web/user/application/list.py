import dataclasses

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.pagination import pagination as shared_pagination

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.user import user_id as shared_user_id
from chackra_web.shared.domain.model.specifications import builder as shared_specification_builder

from chackra_web.user.domain.models import user as domain_user, repositories as user_repositories


@dataclasses.dataclass
class ListUserMatchingDTO:
    pagination: shared_pagination.Pagination


class ListCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    user_repository:  user_repositories.UserBaseRepository[domain_user.User, shared_user_id.UserId]
    specification_builder: shared_specification_builder.SpecificationBuilder

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger

        self.user_repository = dependencies.repository_store.build(
            user_repositories.UserBaseRepository[domain_user.User, shared_user_id.UserId]
        )
        self.specification_builder = dependencies.specification_builder

    def execute(self, list_user_matching_dto: ListUserMatchingDTO) -> shared_pagination.Paginator:
        if filters := list_user_matching_dto.pagination.filters:
            filters.inject_all_to_prefix("tu")
            if search_specification := filters.find_by_attribute("search"):
                print("search - ", search_specification)
                name_like_specification = self.specification_builder.build(
                    "name",
                    "ilike",
                    search_specification.value,
                    prefix="tu"
                )
                last_name_like_specification = self.specification_builder.build(
                    "last_name",
                    "ilike",
                    search_specification.value,
                    prefix="tu"
                )
                email_like_specification = self.specification_builder.build(
                    "email",
                    "ilike",
                    search_specification.value,
                    prefix="tu"
                )
                username_like_specification = self.specification_builder.build(
                    "username",
                    "ilike",
                    search_specification.value,
                    prefix="tu"
                )
                filtered_or_like = (
                        name_like_specification |
                        email_like_specification |
                        username_like_specification |
                        last_name_like_specification
                )
                list_user_matching_dto.pagination.filters = list_user_matching_dto.pagination.filters.find_and_replace_by_attribute(
                    "search",
                    filtered_or_like
                )

        return self.user_repository.matching(list_user_matching_dto.pagination)