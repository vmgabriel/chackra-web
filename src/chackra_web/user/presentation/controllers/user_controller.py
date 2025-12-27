
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.applications import register_user

from chackra_web.user.domain.models import exceptions as user_exceptions
from chackra_web.auth.domain.models import exceptions as auth_exceptions


class UserController(shared_controller.WebController):
    def get_routes(self) -> List[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/users/create",
                handler=self.register_page,
                methods=[shared_route.HttpMethod.GET],
                name="user.register_get",
                template="user/register.html"
            ),
            shared_route.RouteDefinition(
                path="/users/create",
                handler=self.save_user,
                methods=[shared_route.HttpMethod.POST],
                name="user.register_save",
                template="user/register.html"
            ),
        ]

    def register_page(self) -> dict:
        return {"title": "Home"}

    def save_user(self, request: shared_route.RequestData):
        to_register = register_user.RegisterUserDTO(
            email=request.body.get("email", ""),
            password=request.body.get("password", ""),
            name=request.body.get("name", ""),
            last_name=request.body.get("last_name", ""),
            username=request.body.get("username", ""),
        )
        try:
            new_user_recorded = register_user.ApplicationRegisterUser(
                dependencies=self.dependencies
            ).execute(to_register)
            return shared_route.RouteResponse(
                flash_message="Usuario Registrado Correctamente",
                status_code=300,
                redirection="auth.home",
                session=shared_route.Session(
                    status=shared_route.StatusSession.SUCCESS,
                    user_id=new_user_recorded.user_id.value,
                    auth_id=new_user_recorded.auth_id.value,
                    email=new_user_recorded.email,
                    role=new_user_recorded.role,
                ),
            )
        except (user_exceptions.UserExistsException, auth_exceptions.AuthExistsException):
            return {
                "errors": [
                    {
                        "title": "Usuario ya registrado",
                        "description": "El usuario ya existe, quizas quiera iniciar sesion",
                    }
                ]
            }