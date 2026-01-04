from typing import List

from chackra_web.shared.domain.model.web import controller as shared_controller, route as shared_route

from chackra_web.auth.domain.services.middlewares import login_required


class FoodTrackHomeController(shared_controller.WebController):
    def get_routes(self) -> List[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/food-track",
                handler=self.home_food_track_get,
                methods=[shared_route.HttpMethod.GET],
                name="food_track.home",
                template="food_track/home.html",
                middleware=[login_required.login_required(roles=["USER", "ADMIN"])],
                getters_allowed=[],
            ),
        ]

    def home_food_track_get(self, user: shared_route.Session) -> dict:
        return {
            "user": user,
        }
