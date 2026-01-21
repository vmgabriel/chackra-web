from chackra_web.user.domain.models import additional_user, repositories as user_repositories
from chackra_web.shared.domain.model.user import user_id, additional_user_id


def get_by_user_id(
    additional_user_id: user_id.UserId,
    additional_user_repository: user_repositories.AdditionalUserRepository[
        additional_user.UserAdditionalInformation,
        additional_user_id.AdditionalUserId
    ],
) -> additional_user.UserAdditionalInformation | None:
    return additional_user_repository.find_by_user_id(additional_user_id)
