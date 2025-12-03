
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.applications import register_user


class UserController(shared_controller.WebController):
    def get_routes(self) -> List[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/backoffice/users",
                handler=self.list_users,
                methods=[shared_route.HttpMethod.GET],
                name="user.list_users_get",
                template="user/list.html"
            ),
        ]

    def list_users(self) -> dict:
        return {
            "pagination": {
                "has_prev": False,
                "has_next": True,
                "next_page": 2,
                "current": 1,
                "pages": [1, 2, 3, 4]
            },
            "users": [
                {
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                },
                {
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                },
                {
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                },
                {
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                },
                {
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                },
                {
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                },
                {
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                },
                {
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                },
                {
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                },
                {
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                },
                {
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                },
                {
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                },{
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                },
                {
                    "id": 1,
                    "avatar": "https://avatars.githubusercontent.com/u/10355449?v=4",
                    "initials": "JD",
                    "name": "Juan",
                    "email": "juanito.123@gmail.com",
                    "role": "user",
                    "status": "active",
                    "last_login": "2023-01-01T00:00:00",
                    "created_at": "2023-01-01T00:00:00",
                }
            ]
        }