from chackra_web.web.domain.web import app as domain_web_app

from chackra_web.shared.domain.model.web import route as shared_route, controller as shared_controller
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.web.infraestructure.configuration import factory as infraestructure_configuration_factory
from chackra_web.web.infraestructure.web import factory as infraestructure_web_factory

from chackra_web.auth.presentation.controllers import auth_controller
from chackra_web.user.presentation.controllers import user_controller, list_users_controller


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


def get_configuration() -> shared_configuration.Configuration:
    factory_configuration = infraestructure_configuration_factory.ConfigurationFactory(env="DEV")
    return factory_configuration.build()


def get_web_app(configuration: shared_configuration.Configuration) -> domain_web_app.WebAppFactory:
    factory_web = infraestructure_web_factory.WebApplicationFactory()
    return factory_web.build(configuration=configuration)


def inject_controllers(web: domain_web_app.WebAppFactory, controllers: list[shared_controller.WebController]):
    for controller in controllers:
        web.add_controller(controller)


def create_app() -> object:
    configuration = get_configuration()

    web = get_web_app(configuration)

    controllers = [
        HomeWebController(),
        ContactWebController(),
        AboutWebController(),

        auth_controller.AuthController(),
        user_controller.UserController(),
        list_users_controller.UserController(),
    ]
    inject_controllers(web, controllers)

    return web.build()


app = create_app()


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()

