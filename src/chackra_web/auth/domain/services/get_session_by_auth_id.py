from chackra_web.shared.domain.model.web import route as shared_route
from chackra_web.shared.domain.model.auth import auth_id as shared_auth_id
from chackra_web.auth.domain.models import auth as domain_auth, repositories as auth_repositories
from chackra_web.auth.domain.services import get_by_id as auth_get_by_id


def get_session_by_auth_id(
    auth_id: str,
    auth_repository: auth_repositories.AuthBaseRepository[domain_auth.AuthUser, shared_auth_id.AuthId],
) -> shared_route.Session | None:
    auth_data = auth_get_by_id.get_by_id(auth_id=shared_auth_id.AuthId(value=auth_id), auth_repository=auth_repository)
    return shared_route.Session(
        status=shared_route.StatusSession.TRANSIT,
        auth_id=auth_data.id.value,
        user_id=auth_data.user_id.value,
        email=auth_data.email,
        role=auth_data.auth_role,
    )