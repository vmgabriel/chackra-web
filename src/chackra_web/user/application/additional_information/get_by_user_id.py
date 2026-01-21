from chackra_web.user.domain.models import additional_user as domain_additional_user

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.user import additional_user_id as domain_additional_user_id
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration

from chackra_web.user.domain.models import (
    additional_user as additional_user_domain,
    repositories as user_repositories
)
from chackra_web.user.domain.services.additional_information import get_by_user_id as services_get_by_user_id


class AdditionalInformationGetByUserByIdCommand(object):
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    additional_user_repository:  user_repositories.AdditionalUserRepository[
        additional_user_domain.UserAdditionalInformation,
        domain_additional_user_id.AdditionalUserId
    ]
    configuration: shared_configuration.Configuration

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger
        self.additional_user_repository = dependencies.repository_store.build(
            user_repositories.AdditionalUserRepository[
                additional_user_domain.UserAdditionalInformation,
                domain_additional_user_id.AdditionalUserId
            ]
        )
        self.configuration = dependencies.configuration

    def execute(self, user_id: domain_additional_user_id) -> domain_additional_user.UserAdditionalInformation | None:
        return services_get_by_user_id.get_by_user_id(user_id, self.additional_user_repository)
