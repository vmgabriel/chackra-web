
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.domain.model.pagination import pagination as shared_pagination

from chackra_web.auth.domain.services.middlewares import login_required

from chackra_web.user.application import list as application_user_list


class UserController(shared_controller.WebController):
    def get_routes(self) -> List[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/backoffice/users",
                handler=self.list_users,
                methods=[shared_route.HttpMethod.GET],
                name="user.list_users_get",
                template="user/list.html",
                middleware=[login_required.login_required(roles=["ADMIN"])],
                getters_allowed=["active", "roles", "id", "search"],
            ),
        ]

    def list_users(self, pagination: shared_pagination.Pagination, user: shared_route.Session) -> dict:
        paginator = application_user_list.ListCommand(
            dependencies=self.dependencies
        ).execute(
            list_user_matching_dto=application_user_list.ListUserMatchingDTO(
                pagination=pagination
            )
        )

        return {
            "paginator": paginator,
            "user": user,
        }