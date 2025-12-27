from chackra_web.user.domain.models import user as domain_user, repositories as user_repositories
from chackra_web.shared.domain.model.user import user_id as shared_user_id


def get_by_id(
    user_id: shared_user_id.UserId,
    user_repository: user_repositories.UserBaseRepository[domain_user.User, shared_user_id.UserId],
) -> domain_user.User | None:
    return user_repository.find_by_id(user_id)
