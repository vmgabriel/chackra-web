
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route

from chackra_web.auth.domain.services.middlewares import login_required

from chackra_web.food_track.domain.models import exceptions as domain_exceptions
from chackra_web.food_track.application.to_buy import (
    create as application_to_buy_create,
    delete as application_to_buy_delete,
    update as application_to_buy_update,
    get_by_id as application_to_buy_get_by_id,
)


class ToBuyListController(shared_controller.WebController):
    def get_routes(self) -> List[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/to_buy/create",
                handler=self.create_to_buy_get,
                methods=[shared_route.HttpMethod.GET],
                name="food_track.create_to_buy_get",
                template="food_track/to_buy/upsert.html",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
                getters_allowed=[],
            ),
            shared_route.RouteDefinition(
                path="/to_buy/create",
                handler=self.create_to_buy_post,
                methods=[shared_route.HttpMethod.POST],
                name="food_track.create_to_buy_post",
                template="food_track/to_buy/upsert.html",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
                getters_allowed=[],
            ),
            shared_route.RouteDefinition(
                path="/to_buy/delete",
                handler=self.delete_to_buy_post,
                methods=[shared_route.HttpMethod.POST],
                name="food_track.delete_to_buy_post",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
            ),
            shared_route.RouteDefinition(
                path="/to_buy/<id>/edit",
                handler=self.edit_to_buy_list_get,
                methods=[shared_route.HttpMethod.GET],
                name="food_track.update_to_buy_get",
                template="food_track/to_buy/upsert.html",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
            ),
            shared_route.RouteDefinition(
                path="/to_buy/<id>/edit",
                handler=self.update_to_buy_post,
                methods=[shared_route.HttpMethod.POST],
                name="food_track.update_to_buy_post",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
            ),
            shared_route.RouteDefinition(
                path="/to_buy_list/<id>/items",
                handler=self.show_to_buy_list_get,
                methods=[shared_route.HttpMethod.GET],
                name="food_track.show_to_buy_list_items_get",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
            )
        ]

    def create_to_buy_get(self, user: shared_route.Session) -> dict:
        return {
            "user": user,
        }

    def create_to_buy_post(
        self,
        request: shared_route.RequestData,
    ) -> dict | shared_route.RouteResponse:
        print("request - ", request.body)

        created_to_buy_dbt = application_to_buy_create.CreateToBuyListDTO(
            title=request.body.get("title"),
            description=request.body.get("description"),
        )

        application_to_buy_create.CreateToBuyListCommand(
            dependencies=self.dependencies
        ).execute(create_to_buy_dto=created_to_buy_dbt)

        return shared_route.RouteResponse(
            flash_message="Lista de Compras Creada Correctamente",
            status_code=300,
            redirection="food_track.to_buy_list_get",
        )

    def delete_to_buy_post(self, request: shared_route.RequestData,) -> dict | shared_route.RouteResponse:
        current_id = request.body.get("id")

        if not current_id:
            return {
                "errors": [
                    {
                        "title": "ID Requerido",
                        "description": "El id de la lista de compras es requerido",
                    }
                ]
            }
        try:
            application_to_buy_delete.DeleteToBuyListCommand(dependencies=self.dependencies).execute(
                delete_request=application_to_buy_delete.DeleteToBuyListDTO(id=current_id)
            )
        except domain_exceptions.InventoryItemNotExistsException:
            return {
                "errors": [
                    {
                        "title": "To Buy List not Found",
                        "description": "La lista de compras no existe",
                    }
                ]
            }

        return {
            "message": "ok",
        }

    def update_to_buy_post(
            self,
            id: str,
            request: shared_route.RequestData,
    ) -> dict | shared_route.RouteResponse:
        try:
            application_to_buy_update.UpdateToBuyListCommand(
                dependencies=self.dependencies
            ).execute(
                application_to_buy_update.UpdateToBuyListRequestDTO(
                    id=id,
                    title=request.body.get("title"),
                    description=request.body.get("description"),
                    is_bought=(request.body.get("is_bought").lower() == "true"),
                )
            )
        except ValueError as e:
            return {
                "errors": [
                    {
                        "title": "Body not valid",
                        "description": str(e),
                    }
                ]
            }
        except domain_exceptions.ToBuyListNotFoundException:
            return shared_route.RouteResponse(
                status_code=404,
                redirection="auth.not_found",
                flash_message="To Buy List not found",
            )
        return shared_route.RouteResponse(
            flash_message="To buy list Updated",
            status_code=300,
            redirection="food_track.to_buy_list_get",
        )

    def edit_to_buy_list_get(self, id: str, user: shared_route.Session) -> dict | shared_route.RouteResponse:
        try:
            to_buy_list = application_to_buy_get_by_id.GetByIdToBuyListCommand(
                dependencies=self.dependencies
            ).execute(
                application_to_buy_get_by_id.GetByIdToBuyListIdDTO(id=id)
            )
            return {
                "item": to_buy_list,
                "user": user,
            }
        except domain_exceptions.ToBuyListNotFoundException:
            return shared_route.RouteResponse(
                status_code=404,
                redirection="auth.not_found",
                flash_message="Lista de Compras No Encontrado",
            )

    def show_to_buy_list_get(self, id: str) -> dict | shared_route.RouteResponse:
        return {"id": id}

