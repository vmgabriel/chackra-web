from chackra_web.shared.domain.model.web import route as shared_route, controller as shared_controller

from chackra_web.auth.presentation.controllers import auth_controller
from chackra_web.user.presentation.controllers import user_controller, list_users_controller
from chackra_web.food_track.presentation.controllers import (
    list_inventory_controller,
    inventory_controller, home as food_track_home
)
from chackra_web.food_track.presentation.controllers.to_buy import (
    list as to_buy_list_controller,
    entity as to_buy_entity_controller
)
from chackra_web.entrypoints import dependences_builder


class HomeWebController(shared_controller.WebController):
    def index(self):
        return {"message": "Hello World!"}

    def get_routes(self) -> list[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/",
                handler=self.index,
                methods=[shared_route.HttpMethod.GET],
                name="home",
                template="home.html"
            ),
        ]


class ContactWebController(shared_controller.WebController):
    def contact(self):
        return {"message": "Hello World!"}

    def get_routes(self) -> list[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/contact",
                handler=self.contact,
                methods=[shared_route.HttpMethod.GET],
                name="contact",
                template="contact.html"
            ),
        ]


class AboutWebController(shared_controller.WebController):
    def contact(self):
        return {"message": "Hello World!"}

    def get_routes(self) -> list[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/about",
                handler=self.contact,
                methods=[shared_route.HttpMethod.GET],
                name="about",
                template="about.html"
            ),
        ]


class HealthCheckController(shared_controller.WebController):
    def health(self):
        return {"status": "ok"}

    def get_routes(self) -> list[shared_route.RouteDefinition]:
        return [
            shared_route.RouteDefinition(
                path="/health",
                handler=self.health,
                methods=[shared_route.HttpMethod.GET],
                name="health",
            ),
        ]


def create_app() -> object:
    extended_dependencies = dependences_builder.get_extended_dependences()
    handlers = dependences_builder.build_converters_handlers(configuration=dependences_builder.configuration)

    web = dependences_builder.get_web_app(extended_dependencies.configuration, extended_dependencies, handlers)

    controllers = [
        HomeWebController,
        ContactWebController,
        AboutWebController,
        HealthCheckController,

        auth_controller.AuthController,
        user_controller.UserController,
        list_users_controller.UserController,
        # Food track
        list_inventory_controller.ListInventoryController,
        inventory_controller.InventoryController,
        food_track_home.FoodTrackHomeController,
        to_buy_list_controller.ListToBuyController,
        to_buy_list_controller.ListToBuyItemController,
        to_buy_entity_controller.ToBuyListController,
        to_buy_entity_controller.ToBuyItemController,
    ]
    dependences_builder.inject_controllers(web, extended_dependencies, controllers)

    return web.build()


app = create_app()


def main():
    app.run(debug=True, port=dependences_builder.configuration.port, host=dependences_builder.configuration.host)


if __name__ == "__main__":
    main()

