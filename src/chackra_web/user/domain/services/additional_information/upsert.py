from chackra_web.user.domain.models import additional_user as domain_additional_user, repositories as user_repositories
from chackra_web.shared.domain.model.user import additional_user_id

from chackra_web.user.domain.services.additional_information import get_by_user_id as services_get_by_user_id


def upsert(
    update_additional_information: domain_additional_user.UpdateUserAdditionalInformation,
    additional_user_repository: user_repositories.AdditionalUserRepository[
        domain_additional_user.UserAdditionalInformation,
        additional_user_id.AdditionalUserId
    ],
) -> domain_additional_user.UserAdditionalInformation:
    additional_user = services_get_by_user_id.get_by_user_id(
        additional_user_id=update_additional_information.user_id,
    additional_user_repository=additional_user_repository,
    )
    if additional_user:
        current_additional_user = additional_user.update(update_dto=update_additional_information)
        additional_user_repository.update(
            id=additional_user.id,
            entity=current_additional_user
        )
        return current_additional_user

    current_additional_user = domain_additional_user.UserAdditionalInformation.create(create_dto=update_additional_information)
    additional_user_repository.create(current_additional_user)
    return current_additional_user

