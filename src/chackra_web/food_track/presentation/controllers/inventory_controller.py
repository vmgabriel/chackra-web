
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.domain.model.quantity import quantity as shared_quantity
from chackra_web.food_track.domain.models import exceptions as inventory_exceptions
from chackra_web.food_track.application.inventory import (
    create as inventory_item_create,
    get_by_id as inventory_item_get_by_id,
    delete as inventory_item_delete,
    update as inventory_item_update,
)

from chackra_web.auth.domain.services.middlewares import login_required


class InventoryController(shared_controller.WebController):
    def get_routes(self) -> List[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/inventory/items/create",
                handler=self.create_get,
                methods=[shared_route.HttpMethod.GET],
                name="food_track.create_inventory_get",
                template="food_track/create_inventory.html",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
                getters_allowed=[],
            ),
            shared_route.RouteDefinition(
                path="/inventory/items/create",
                handler=self.create_post,
                methods=[shared_route.HttpMethod.POST],
                name="food_track.create_inventory_post",
                template="food_track/create_inventory.html",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
                getters_allowed=[],
            ),
            shared_route.RouteDefinition(
                path="/inventory/items/delete",
                handler=self.delete_inventory_post,
                methods=[shared_route.HttpMethod.POST],
                name="food_track.delete_inventory_post",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
            ),
            shared_route.RouteDefinition(
                path="/inventory/items/<id>/edit",
                handler=self.edit_inventory_item_get,
                methods=[shared_route.HttpMethod.GET],
                name="food_track.edit_inventory_item_get",
                template="food_track/create_inventory.html",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
            ),
            shared_route.RouteDefinition(
                path="/inventory/items/<id>/edit",
                handler=self.edit_inventory_item_post,
                methods=[shared_route.HttpMethod.POST],
                name="food_track.edit_inventory_post",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
            ),
        ]

    def create_get(self, user: shared_route.Session) -> dict:
        return {
            "user": user,
        }

    def create_post(
            self,
            user: shared_route.Session,
            request: shared_route.RequestData
    ) -> shared_route.RouteResponse | dict:

        try:
            inventory_item_create.CreateInventoryCommand(dependencies=self.dependencies).execute(
                create_inventory_dto=inventory_item_create.CreateInventoryDTO(
                    name=request.body.get("name", ""),
                    quantity=shared_quantity.Quantity(
                        value=float(request.body.get("quantity_value", "")),
                        measure_unit=request.body.get("quantity_measure_unit", "")
                    ),
                )
            )
        except inventory_exceptions.InventoryItemExistsException:
            return {
                "user": user,
                "errors": [
                    {
                        "title": "Item ya esta en el inventario",
                        "description": "El usuario esta en el inventario, recomendamos buscarlo",
                    }
                ]
            }


        return shared_route.RouteResponse(
            flash_message="Inventario Item Creado Correctamente",
            status_code=300,
            redirection="food_track.list_inventory_get",
        )

    def delete_inventory_post(
            self,
            request: shared_route.RequestData,
            user: shared_route.Session
    ) -> dict:
        current_id = request.body.get("id")
        if not current_id:
            return {
                "errors": [
                    {
                        "title": "ID Requerido",
                        "description": "El id del item es requerido",
                    }
                ]
            }

        try:
            inventory_item_delete.DeleteInventoryItemCommand(dependencies=self.dependencies).execute(
                delete_request=inventory_item_delete.DeleteInventoryItemDTO(id=current_id)
            )
        except inventory_exceptions.InventoryItemNotExistsException:
            return {
                "errors": [
                    {
                        "title": "Inventory Item not Found",
                        "description": "El inventory item no existe",
                    }
                ]
            }

        return {
            "message": "ok",
        }

    def edit_inventory_item_get(self, id: str, user: shared_route.Session) -> dict | shared_route.RouteResponse:
        try:
            inventory_item = inventory_item_get_by_id.GetByIdInventoryItemCommand(
                dependencies=self.dependencies
            ).execute(
                inventory_item_get_by_id.GetByIdInventoryIdDTO(id=id)
            )
            return {
                "item": inventory_item,
                "user": user,
            }
        except inventory_exceptions.InventoryItemNotExistsException:
            return shared_route.RouteResponse(
                status_code=404,
                redirection="auth.not_found",
                flash_message="Inventory Item not found",
            )

    def edit_inventory_item_post(
            self,
            id: str,
            request: shared_route.RequestData,
            user: shared_route.Session
    ) -> dict | shared_route.RouteResponse:
        try:
            inventory_item_update.UpdateInventoryItemCommand(
                dependencies=self.dependencies
            ).execute(
                inventory_item_update.UpdateInventoryItemRequestDTO(
                    id=id,
                    name=request.body.get("name"),
                    quantity_value=request.body.get("quantity_value"),
                    quantity_measure_unit=shared_quantity.MeasureUnitType(request.body.get("quantity_measure_unit")),
                    is_sold_out=bool(request.body.get("is_sold_out").lower() == "true"),
                )
            )
        except ValueError as e:
            return {
                "user": user,
                "errors": [
                    {
                        "title": "Body not valid",
                        "description": str(e),
                    }
                ]
            }
        except inventory_exceptions.InventoryItemNotExistsException:
            return shared_route.RouteResponse(
                status_code=404,
                redirection="auth.not_found",
                flash_message="Inventory Item not found",
            )
        return shared_route.RouteResponse(
            flash_message="Inventory Item Updated",
            status_code=300,
            redirection="food_track.list_inventory_get",
        )
