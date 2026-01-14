
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route
from chackra_web.shared.domain.model.pagination import pagination as shared_pagination

from chackra_web.food_track.application.to_buy import list_lister as to_buy_lister, get_by_id as application_get_by_id

from chackra_web.auth.domain.services.middlewares import login_required

class ListToBuyController(shared_controller.WebController):
    def get_routes(self) -> List[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/to-buy",
                handler=self.list_to_buy,
                methods=[shared_route.HttpMethod.GET],
                name="food_track.to_buy_list_get",
                template="food_track/to_buy/list.html",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
                getters_allowed=["search", ],
            ),
        ]

    def list_to_buy(
            self,
            pagination: shared_pagination.Pagination,
            user: shared_route.Session
    ) -> dict:
        paginator = to_buy_lister.ListToBuyCommand(
            dependencies=self.dependencies
        ).execute(
            list_inventory_item_matching_dto=to_buy_lister.ListToBuyMatchingDTO(
                pagination=pagination
            )
        )

        paginator_extended = shared_pagination.PaginatorExtended.from_paginator(paginator)
        paginator_extended.headers = {"title": "Titulo", "description": "Description", "is_bought": "Ya Comprado?"}
        paginator_extended.title = "Lista de todas las listas de compras"
        paginator_extended.message_delete = (
            "¿Estás seguro de que deseas eliminar esta lista de compras? Esta acción no se puede deshacer."
        )
        paginator_extended.title_delete = "Eliminar Lista de Compras"
        paginator_extended.delete_url = "food_track.delete_to_buy_post"
        paginator_extended.update_url = "food_track.update_to_buy_get"
        paginator_extended.show_url = "food_track.to_buy_items_get"
        paginator_extended.url_current_keys = {}
        paginator_extended.current_endpoint = "food_track.to_buy_list_get"
        paginator_extended.filter_convertion = "filter_to_buy_lists"
        paginator_extended.list_convertion = "list_to_buy_lists"
        paginator_extended.filters = ["search", "is_bought"]

        return {
            "paginator": paginator_extended,
            "user": user,
        }



class ListToBuyItemController(shared_controller.WebController):
    def get_routes(self) -> List[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/to-buy/<id>/items",
                handler=self.list_items_in_to_buy_get,
                methods=[shared_route.HttpMethod.GET],
                name="food_track.to_buy_items_get",
                template="food_track/to_buy/items/list.html",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
                getters_allowed=["search", ],
            ),
        ]

    def list_items_in_to_buy_get(
            self,
            id: str,
            pagination: shared_pagination.Pagination,
            user: shared_route.Session
    ) -> dict | shared_route.RouteResponse:
        paginator = to_buy_lister.ToBuyItemListCommand(
            dependencies=self.dependencies
        ).execute(
            list_to_buy_items_matching_dto=to_buy_lister.ListToBuyItemsMatchingDTO(
                pagination=pagination
            )
        )

        current_list_to_buy = application_get_by_id.GetByIdToBuyListCommand(self.dependencies).execute(
            get_by_id=application_get_by_id.GetByIdToBuyListIdDTO(id=id)
        )

        paginator_extended = shared_pagination.PaginatorExtended.from_paginator(paginator)
        paginator_extended.headers = {"name": "Nombre", "quantity": "Cantidad", "comment": "Comentario"}
        paginator_extended.title = "Lista de elementos de compras"
        paginator_extended.message_delete = (
            "¿Estás seguro de que deseas eliminar este producto de la lista de compras? Esta acción no se puede deshacer."
        )
        paginator_extended.title_delete = "Eliminar Producto de la lista de compras"
        paginator_extended.delete_url = "food_track.delete_to_buy_item_post"
        paginator_extended.update_url = "food_track.edit_to_buy_item_get"
        paginator_extended.show_url = "food_track.show_to_buy_list_items_get"
        paginator_extended.url_current_keys = {"id": id}
        paginator_extended.url_keys = {"to_buy_id": "to_buy_id", "id": "id"}
        paginator_extended.current_endpoint = "food_track.to_buy_list_get"
        paginator_extended.filter_convertion = "filter_to_buy_lists"
        paginator_extended.list_convertion = "list_to_buy_lists"
        paginator_extended.filters = ["search", "name"]

        return {
            "to_buy_list": current_list_to_buy,
            "paginator": paginator_extended,
            "user": user,
        }
