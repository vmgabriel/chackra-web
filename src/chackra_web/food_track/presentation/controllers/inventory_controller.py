
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.domain.model.pagination import pagination as shared_pagination

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

    def create_post(self, request: shared_route.RequestData) -> dict:
        print("Inventory - ", request.body)

        return {}