
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.domain.model.quantity import quantity as shared_quantity
from chackra_web.food_track.domain.models import exceptions as inventory_exceptions
from chackra_web.food_track.application import create_inventory

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
            create_inventory.CreateInventoryCommand(dependencies=self.dependencies).execute(
                create_inventory_dto=create_inventory.CreateInventoryDTO(
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