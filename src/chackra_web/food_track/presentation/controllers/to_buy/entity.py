
from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route

from chackra_web.auth.domain.services.middlewares import login_required


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
        ]

    def create_to_buy_get(self, user: shared_route.Session) -> dict:
        return {
            "user": user,
        }
