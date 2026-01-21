
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.domain.model.pagination import pagination as shared_pagination

from chackra_web.food_track.application.inventory import list as inventory_list

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
                getters_allowed=["search", "state"],
            ),
            shared_route.RouteDefinition(
                path="/inventory/items/search",
                handler=self.list_inventory_item_search_get,
                methods=[shared_route.HttpMethod.GET],
                name="food_track.list_inventory_item_search_get",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
                getters_allowed=["search"],
            )
        ]

    def list_inventory(
            self,
            pagination: shared_pagination.Pagination,
            user: shared_route.Session
    ) -> dict:
        paginator = inventory_list.ListInventoryItemCommand(
            dependencies=self.dependencies
        ).execute(
            list_inventory_item_matching_dto=inventory_list.ListInventoryItemMatchingDTO(
                pagination=pagination
            )
        )

        paginator_extended = shared_pagination.PaginatorExtended.from_paginator(paginator)
        paginator_extended.headers = {"name": "Nombre", "quantity": "Cantidad", "is_sold_out": "Estado"}
        paginator_extended.title = "Lista de Productos en Inventario"
        paginator_extended.message_delete = (
            "¿Estás seguro de que deseas eliminar este Item de Inventario? Esta acción no se puede deshacer."
        )
        paginator_extended.title_delete = "Eliminar Item de Inventario"
        paginator_extended.delete_url = "food_track.delete_inventory_post"
        paginator_extended.update_url = "food_track.edit_inventory_item_get"
        paginator_extended.current_endpoint = "food_track.list_inventory_get"
        paginator_extended.filter_convertion = "filter_inventory"
        paginator_extended.list_convertion = "list_inventory"
        paginator_extended.filters = ["search", "state"]

        return {
            "paginator": paginator_extended,
            "user": user,
        }

    def list_inventory_item_search_get(
            self,
            pagination: shared_pagination.Pagination,
            user: shared_route.Session
    ) -> dict:
        entities = inventory_list.SearchInventoryItemCommand(
            dependencies=self.dependencies
        ).execute(list_inventory_item_matching_dto=inventory_list.SearchInventoryItemMatchingDTO(
            pagination=pagination
        ))

        return {
            "payload": {
                "user": user.user_id,
                "entities": [{
                        "name": entity.name,
                        "id": str(entity.id)
                    } for entity in getattr(entities, "entities", [])
                ],
            },
            "errors": [],
        }
