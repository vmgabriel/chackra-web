from chackra_web.web.domain.web import app as domain_web_app

from chackra_web.shared.domain.model.web import route as shared_route, controller as shared_controller
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.migration import migration as shared_migration

from chackra_web.auth.presentation.controllers import auth_controller
from chackra_web.user.presentation.controllers import user_controller, list_users_controller

from chackra_web.web.infraestructure.configuration import factory as infraestructure_configuration_factory
from chackra_web.web.infraestructure.web import factory as infraestructure_web_factory
from chackra_web.shared.infraestructure.logger import factory as infraestructure_logger_factory
from chackra_web.shared.infraestructure.uow import factory as infraestructure_uow_factory
from chackra_web.shared.infraestructure.migrations import factory as infraestructure_migration_factory

from chackra_web.user.infraestructure import migrations as user_migrations


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


def get_logger(configuration: shared_configuration.Configuration) -> shared_logger.LogAdapter:
    factory_logger = infraestructure_logger_factory.LoggerFactory()
    return factory_logger.build(configuration=configuration)


def get_uow(configuration: shared_configuration.Configuration, logger: shared_logger.LogAdapter) -> shared_uow.UOW:
    factory_uow = infraestructure_uow_factory.UOWFactory()
    return factory_uow.build(configuration=configuration, logger=logger)


def get_migration_handler(
        configuration: shared_configuration.Configuration,
        logger: shared_logger.LogAdapter,
        uow: shared_uow.UOW,
) -> shared_migration.MigratorHandler:
    factory_migration_handler = infraestructure_migration_factory.MigrationFactory()
    return factory_migration_handler.build(configuration=configuration, logger=logger, uow=uow)


def inject_migrations(
        migration_handler: shared_migration.MigratorHandler,
        migrations: list[shared_migration.MigrateHandler],
):
    for migration in migrations:
        migration_handler.add_migration(migration)


def inject_controllers(web: domain_web_app.WebAppFactory, controllers: list[shared_controller.WebController]):
    for controller in controllers:
        web.add_controller(controller)


def create_app() -> object:
    configuration = get_configuration()

    log = get_logger(configuration)

    uow = get_uow(configuration, log)
    migration_handler = get_migration_handler(configuration, log, uow)

    migrations = []
    migrations.extend(user_migrations.get_migration_handlers(configuration=configuration))

    inject_migrations(migration_handler=migration_handler, migrations=migrations)
    migration_handler.pre_execute()
    migration_handler.execute()

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

