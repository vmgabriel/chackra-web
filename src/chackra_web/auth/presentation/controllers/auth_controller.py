
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.domain.model.user import user_id as shared_user_id
from chackra_web.auth.domain.services.middlewares import login_required

from chackra_web.auth.application import login, change_role


class AuthController(shared_controller.WebController):
    def get_routes(self) -> List[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/login",
                handler=self.login_page,
                methods=[shared_route.HttpMethod.GET],
                name="auth.login_get",
                template="auth/login.html"
            ),
            shared_route.RouteDefinition(
                path="/login",
                handler=self.login_submit,
                methods=[shared_route.HttpMethod.POST],
                name="auth.login_verify",
                template="auth/login.html"
            ),
            shared_route.RouteDefinition(
                path="/home",
                handler=self.home,
                methods=[shared_route.HttpMethod.GET],
                name="auth.home",
                template="main.html",
                middleware=[login_required.login_required(roles=["ADMIN", "USER"])],
            ),
            shared_route.RouteDefinition(
                path="/login/recovery",
                handler=self.recovery,
                methods=[shared_route.HttpMethod.GET],
                name="auth.recovery",
                template="auth/recovery.html"
            ),
            shared_route.RouteDefinition(
                path="/backoffice/login/change-role",
                handler=self.change_role,
                methods=[shared_route.HttpMethod.POST],
                name="auth.change-role_post",
            ),
            shared_route.RouteDefinition(
                path="/logout",
                handler=self.logout,
                methods=[shared_route.HttpMethod.GET],
                name="auth.logout",
                template="main.html",
                middleware=[login_required.login_required(roles=["ADMIN", "USER"])],
            )
        ]

    def home(self, user: shared_route.Session) -> dict:
        return {"title": "Home", "user": user}

    def login_page(self) -> dict:
        return {
            "title": "Iniciar Sesión",
            "form": {}
        }

    def login_submit(self, request: shared_route.RequestData) -> shared_route.RouteResponse | dict:

        login_data = login.LoginDTO(
            email=request.body.get("email", ""),
            password=request.body.get("password", ""),
        )
        verification = login.LoginCommand(dependencies=self.dependencies).execute(login_data)

        if verification:
            return shared_route.RouteResponse(
                flash_message="Login correcto",
                status_code=300,
                redirection="auth.home",
                session=shared_route.Session(
                    status=shared_route.StatusSession.SUCCESS,
                    user_id=verification.user_id.value,
                    auth_id=verification.id.value,
                    email=verification.email,
                    role=verification.auth_role,
                )
            )
        else:
            return shared_route.RouteResponse(
                flash_message="Login no valido",
                status_code=300,
                redirection="auth.login_get",
            )

    def logout(self, user: shared_route.Session):
        return shared_route.RouteResponse(
            flash_message="Logout hecho correctamente",
            status_code=300,
            redirection="home",
            session=shared_route.Session(
                status=shared_route.StatusSession.LOGOUT,
                user_id=user.user_id,
                auth_id=user.auth_id,
                email=user.email,
                role=user.role,
            )
        )

    def recovery(self):
        return {}

    def change_role(self, request: shared_route.RequestData) -> shared_route.RouteResponse | dict:
        change_role_dto = change_role.ChangeRoleDTO(
            user_id=shared_user_id.UserId(value=request.body.get("user_id")),
            role=request.body.get("role"),
        )
        change_role.ChangeRoleCommand(dependencies=self.dependencies).execute(change_role_dto)
        return shared_route.RouteResponse(
            flash_message="Cambiado Satisfactoriamente el rol de usuario",
            status_code=300,
            redirection="user.list_users_get",
        )