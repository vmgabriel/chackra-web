
from chackra_web.auth.domain.models import auth as domain_auth, repositories as auth_repositories
from chackra_web.shared.domain.model.user import user_id as domain_user_id
from chackra_web.shared.domain.model.auth import auth_id as shared_auth_id
from chackra_web.auth.domain.models import repositories as auth_repositories


def get_by_user_id(
    user_id: domain_user_id.UserId,
    auth_repository: auth_repositories.AuthBaseRepository[domain_auth.AuthUser, shared_auth_id.AuthId]
) -> domain_auth.AuthUser | None:
    return auth_repository.find_by_user_id(user_id=user_id)
