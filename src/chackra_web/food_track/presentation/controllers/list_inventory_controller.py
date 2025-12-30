
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.domain.model.pagination import pagination as shared_pagination

from chackra_web.auth.domain.services.middlewares import login_required


class ListInventoryController(shared_controller.WebController):
    def get_routes(self) -> List[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/inventory/items",
                handler=self.list_inventory,
                methods=[shared_route.HttpMethod.GET],
                name="food_track.list_inventory_get",
                template="food_track/list_inventory.html",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
                getters_allowed=[],
            ),
        ]

    def list_inventory(self, user: shared_route.Session) -> dict:
        return {
            "paginator": {"entities": [], "total_pages": 1},
            "user": user,
        }