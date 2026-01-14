
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.domain.model.quantity import quantity as shared_quantity

from chackra_web.auth.domain.services.middlewares import login_required

from chackra_web.food_track.domain.models import exceptions as domain_exceptions
from chackra_web.food_track.application.to_buy import (
    create as application_to_buy_create,
    delete as application_to_buy_delete,
    update as application_to_buy_update,
    get_by_id as application_to_buy_get_by_id,
)
from chackra_web.food_track.application import adding_item_into_to_buy_list


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


class ToBuyItemController(shared_controller.WebController):
    def get_routes(self) -> List[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/to_buy/<to_buy_id>/create",
                handler=self.create_to_buy_item_get,
                methods=[shared_route.HttpMethod.GET],
                name="food_track.create_to_buy_item_get",
                template="food_track/to_buy/items/upsert.html",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
                getters_allowed=[],
            ),
            shared_route.RouteDefinition(
                path="/to_buy/<to_buy_id>/create",
                handler=self.create_to_buy_item_post,
                methods=[shared_route.HttpMethod.POST],
                    name="food_track.create_to_buy_item_post",
                template="food_track/to_buy/upsert.html",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
                getters_allowed=[],
            ),
        ]

    def create_to_buy_item_get(
            self,
            to_buy_id: str,
            user: shared_route.Session,
    ) -> dict | shared_route.RouteResponse:
        print(to_buy_id)
        return {
            "to_buy_id": to_buy_id,
            "user": user,
        }

    def create_to_buy_item_post(
        self,
        to_buy_id: str,
        request: shared_route.RequestData,
    ) -> dict | shared_route.RouteResponse:
        print("request - ", request.body)

        try:
            adding_item_into_to_buy_list.AddingItemIntoToBuyListCommand(dependencies=self.dependencies).execute(
                adding_item_into_to_buy_list_dto=adding_item_into_to_buy_list.AddingItemIntoToBuyListDTO(
                    to_buy_id=to_buy_id,
                    inventory_id=request.body.get("inventory_id"),
                    comment=request.body.get("comment"),
                    quantity=shared_quantity.Quantity(
                        value=float(request.body.get("quantity_value", "")),
                        measure_unit=request.body.get("quantity_measure_unit", "")
                    ),
                )
            )
        except domain_exceptions.InventoryItemNotExistsException:
            return {
                "errors": [
                    {
                        "title": "Inventory item not found",
                        "description": "Item del inventario no encontrado",
                    }
                ]
            }


        return shared_route.RouteResponse(
            flash_message="Item de la Lista de Compras creado Correctamente",
            status_code=300,
            redirection="food_track.to_buy_items_get",
            redirection_variables={"id": to_buy_id}
        )