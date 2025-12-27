
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.auth.domain.services.middlewares import login_required

from chackra_web.auth.application import login


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
                middleware=[login_required.login_required(roles=["ADMIN", "USER"])]
            ),
            shared_route.RouteDefinition(
                path="/login/recovery",
                handler=self.recovery,
                methods=[shared_route.HttpMethod.GET],
                name="auth.recovery",
                template="auth/recovery.html"
            )
        ]

    def home(self) -> dict:
        return {"title": "Home"}

    def login_page(self) -> dict:
        return {
            "title": "Iniciar Sesión",
            "form": {}
        }

    def login_submit(self, request) -> shared_route.RouteResponse | dict:
        data = request.form

        login_data = login.LoginDTO(
            email=data.get("email", ""),
            password=data.get("password", ""),
        )
        verification = login.LoginCommand("").execute(login_data)
        if verification:
            return shared_route.RouteResponse(
                flash_message="Login correcto",
                status_code=300,
                redirection="auth.home",
            )
        else:
            return shared_route.RouteResponse(
                flash_message="Login incorrecto",
                status_code=300,
                redirection="auth.login_get",
            )

    def logout(self):
        return {}

    def recovery(self):
        return {}