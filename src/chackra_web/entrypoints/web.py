from chackra_web.domain.web import app as domain_web_app

from chackra_web.domain.shared import configuration as shared_configuration
from chackra_web.infraestructure.configuration import factory as infraestructure_configuration_factory
from chackra_web.infraestructure.web import factory as infraestructure_web_factory


class HomeWebController(domain_web_app.WebController):
    def index(self):
        return {"message": "Hello World!"}

    def get_routes(self) -> list[domain_web_app.RouteDefinition]:
        return [
            domain_web_app.RouteDefinition(
                path="/",
                handler=self.index,
                methods=[domain_web_app.HttpMethod.GET],
                name="home",
                template="home.html"
            ),
        ]


class ContactWebController(domain_web_app.WebController):
    def contact(self):
        return {"message": "Hello World!"}

    def get_routes(self) -> list[domain_web_app.RouteDefinition]:
        return [
            domain_web_app.RouteDefinition(
                path="/contact",
                handler=self.contact,
                methods=[domain_web_app.HttpMethod.GET],
                name="contact",
                template="contact.html"
            ),
        ]


class AboutWebController(domain_web_app.WebController):
    def contact(self):
        return {"message": "Hello World!"}

    def get_routes(self) -> list[domain_web_app.RouteDefinition]:
        return [
            domain_web_app.RouteDefinition(
                path="/about",
                handler=self.contact,
                methods=[domain_web_app.HttpMethod.GET],
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


def create_app() -> object:
    configuration = get_configuration()

    web = get_web_app(configuration)

    controllers = [
        HomeWebController(),
        ContactWebController(),
        AboutWebController()
    ]

    for controller in controllers:
        web.add_controller(controller)

    return web.build()


app = create_app()


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()

