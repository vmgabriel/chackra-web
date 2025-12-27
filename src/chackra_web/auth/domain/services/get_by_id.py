from chackra_web.auth.domain.models import auth as domain_auth, repositories as auth_repositories
from chackra_web.shared.domain.model.auth import auth_id as shared_auth_id


def get_by_id(
    auth_id: shared_auth_id.AuthId,
    auth_repository: auth_repositories.AuthBaseRepository[domain_auth.AuthUser, shared_auth_id.AuthId]
) -> domain_auth.AuthUser | None:
    return auth_repository.find_by_id(auth_id)
