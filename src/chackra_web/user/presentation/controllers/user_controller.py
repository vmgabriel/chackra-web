
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.applications import register_user


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

    def save_user(self, request):
        data = request.form

        to_register = register_user.RegisterUserDTO(
            email=data.get("email", ""),
            password=data.get("password", ""),
            name=data.get("name", ""),
            last_name=data.get("last_name", ""),
        )
        print(f"To Register User: {to_register}")
        try:
            new_user_recorded = register_user.ApplicationRegisterUser(dependencies="...").execute(to_register)
            print(f"New User Recorded: {new_user_recorded}")
            return shared_route.RouteResponse(
                flash_message="Usuario Registrado Correctamente",
                status_code=300,
                redirection="auth.home",
            )
        except Exception as exc:
            print(f"Error Registering User: {exc}")
            return {
                "title": "Home",
                "error": str(exc)
            }