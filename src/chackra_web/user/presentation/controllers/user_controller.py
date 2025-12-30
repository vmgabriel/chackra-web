
from typing import List, Any

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route

from chackra_web.user.domain.models import exceptions as user_exceptions
from chackra_web.auth.domain.models import exceptions as auth_exceptions

from chackra_web.shared.domain.model.user import user_id as shared_user_id

from chackra_web.user.application import get_by_id as user_get_by_id
from chackra_web.shared.applications import register_user, delete_user


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
            shared_route.RouteDefinition(
                path="/users/delete",
                handler=self.delete,
                methods=[shared_route.HttpMethod.POST],
                name="user.delete_post",
                template="user.list.html"
            ),
            shared_route.RouteDefinition(
                path="/users/me",
                handler=self.get_profile,
                methods=[shared_route.HttpMethod.GET],
                name="user.profile_get",
                template="user/profile.html"
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

    def get_profile(self, user: shared_route.Session) -> Any:
        current_user = user_get_by_id.GetByIdUserCommand(
            dependencies=self.dependencies
        ).execute(
            get_by_id_user_dto=user_get_by_id.GetByIDUserDTO(user_id=user.user_id)
        )
        if not current_user:
            return shared_route.RouteResponse(
                flash_message="Usuario no encontrado",
                status_code=300,
                redirection="auth.home",
            )
        return {"title": "Perfil", "user": user, "user_data": current_user.model_dump()}

    def delete(self, request: shared_route.RequestData) -> shared_route.RouteResponse:
        to_delete = delete_user.DeleteUserDTO(
            user_id=shared_user_id.UserId(value=request.body.get("user_id", "")),
        )
        delete_user.ApplicationDeleteUser(dependencies=self.dependencies).execute(to_delete)
        return shared_route.RouteResponse(
            flash_message="Usuario Eliminado Correctamente",
            status_code=300,
            redirection="user.list_users_get",
        )