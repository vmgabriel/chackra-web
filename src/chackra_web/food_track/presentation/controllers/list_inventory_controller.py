
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.domain.model.pagination import pagination as shared_pagination

from chackra_web.food_track.application import list_inventory_item as application_list_inventory_item

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

    def list_inventory(
            self,
            pagination: shared_pagination.Pagination,
            user: shared_route.Session
    ) -> dict:
        paginator = application_list_inventory_item.ListInventoryItemCommand(dependencies=self.dependencies).execute(
            list_inventory_item_matching_dto=application_list_inventory_item.ListInventoryItemMatchingDTO(
                pagination=pagination
            )
        )

        return {
            "paginator": paginator,
            "user": user,
        }