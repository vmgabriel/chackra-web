
from typing import List, Any
import datetime
import json

from chackra_web.user.domain.models import exceptions as user_exceptions
from chackra_web.auth.domain.models import exceptions as auth_exceptions

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.domain.model.user import user_id as shared_user_id

from chackra_web.auth.domain.services.middlewares import login_required

from chackra_web.user.application import get_by_id as user_get_by_id
from chackra_web.user.application.additional_information import (
    upsert as additional_upsert,
    get_by_user_id as application_get_by_user_id,
)
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
            shared_route.RouteDefinition(
                path="/users/me/settings",
                handler=self.settings_me_get,
                methods=[shared_route.HttpMethod.GET],
                name="user.settings_me_get",
                template="user/settings.html",
                middleware=[login_required.login_required(roles=["ADMIN", "USER"])],
            ),
            shared_route.RouteDefinition(
                path="/users/me/settings",
                handler=self.settings_me_post,
                methods=[shared_route.HttpMethod.POST],
                name="user.settings_me_post",
                middleware=[login_required.login_required(roles=["ADMIN", "USER"])],
            )
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

    def settings_me_get(self, user: shared_route.Session) -> shared_route.RouteResponse | dict:
        entity = application_get_by_user_id.AdditionalInformationGetByUserByIdCommand(
            dependencies=self.dependencies
        ).execute(user.get_user_id_default())
        settings_result: dict[str, Any] = {
            "user": user,
        }
        if entity:
            work_schedule_dict = {}
            for day, schedule in entity.work_schedule.model_dump().items():
                work_schedule_dict[day] = {
                    'start': schedule['start'].strftime('%H:%M') if schedule['start'] else '',
                    'end': schedule['end'].strftime('%H:%M') if schedule['end'] else ''
                }

            sleep_phase_dict = {
                'start': entity.sleep_phase.start.strftime('%H:%M') if entity.sleep_phase.start else '',
                'end': entity.sleep_phase.end.strftime('%H:%M') if entity.sleep_phase.end else ''
            }
            settings_result["work_schedule_strings"] = work_schedule_dict
            settings_result["sleep_phase_strings"] = sleep_phase_dict
            settings_result["entity"] = entity
            print("settings_result", settings_result)

        return settings_result

    def settings_me_post(
            self,
            request: shared_route.RequestData,
            user: shared_route.Session
    ) -> shared_route.RouteResponse | dict:
        configuration = self.dependencies.configuration

        additional_upsert_data = additional_upsert.UpsertAdditionalInformationUser(
            user_id=user.get_user_id_default(),
            birth_date=datetime.datetime.strptime(request.body.get("birth_date"), configuration.date_format).date(),
            gender=request.body.get("genre"),
            country=request.body.get("country"),
            height=float(request.body.get("height")),
            weight=float(request.body.get("weight")),
            profession=request.body.get("profession"),
            work_schedule=request.body.get("work_schedule"),
            difficulties=request.body.get("health_difficulties"),
            allergic_product=request.body.get("allergenic_products"),
            lifestyle_product=request.body.get("lifestyle"),
            foods=request.body.get("foods"),
            sleep_time=request.body.get("sleep_phase"),
            with_oven=bool(request.body.get("with_oven")),
        )

        additional_user_saved = additional_upsert.UpsertAdditionalInformationUserCommand(
            dependencies=self.dependencies
        ).execute(additional_upsert_data)

        return {
            "payload": json.loads(additional_user_saved.model_dump_json()),
            "errors": [],
        }
