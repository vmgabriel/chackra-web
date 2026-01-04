
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
                getters_allowed=["active", "role", "id", "search"],
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

        paginator_extended = shared_pagination.PaginatorExtended.from_paginator(paginator)
        paginator_extended.headers = {
            "initials": "",
            "full_name": "Name",
            "username": "Username",
            "auth_role": "Rol",
            "active": "Estado",
            "created_at": "Fecha de Creacion",
        }
        paginator_extended.title = "Lista de Usuarios"
        paginator_extended.message_delete = (
            "¿Estás seguro de que deseas eliminar este Usuario? Esta acción no se puede deshacer."
        )
        paginator_extended.title_delete = "Eliminar Usuario"
        paginator_extended.delete_url = "user.delete_post"
        paginator_extended.current_endpoint = "user.list_users_get"
        paginator_extended.filter_convertion = "filter_user"
        paginator_extended.list_convertion = "list_user"
        paginator_extended.filters = ["search", "active", "role", "id"]

        return {
            "paginator": paginator_extended,
            "user": user,
        }