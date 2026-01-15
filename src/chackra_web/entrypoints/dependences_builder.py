from typing import Type, Callable

from chackra_web.web.domain.web import app as domain_web_app

from chackra_web.shared.domain.model.web import controller as shared_controller
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.migration import migration as shared_migration
from chackra_web.shared.domain.model import (
    dependencies as shared_dependencies,
    extended_dependencies as shared_extended_dependencies
)
from chackra_web.shared.domain.model.repository import builder as shared_builder_repository, factory as shared_factory

from chackra_web.web.infraestructure.configuration import factory as infraestructure_configuration_factory
from chackra_web.web.infraestructure.web import factory as infraestructure_web_factory
from chackra_web.shared.infraestructure.logger import factory as infraestructure_logger_factory
from chackra_web.shared.infraestructure.uow import factory as infraestructure_uow_factory
from chackra_web.shared.infraestructure.migrations import factory as infraestructure_migration_factory
from chackra_web.shared.infraestructure.specifications import factory as infraestructure_specification_factory
from chackra_web.shared.infraestructure.pagination import factory as infraestructure_pagination_factory
from chackra_web.shared.infraestructure.convertion_specification import (
    factory as infraestructure_convertion_specification_factory
)
from chackra_web.shared.infraestructure.convertion_pagination import (
    factory as infraestructure_convertion_pagination_factory
)
from chackra_web.shared.infraestructure.handlers import factory as infraestructure_handler_factory
from chackra_web.food_track.infraestructure.converter import factory as food_track_converter_factory
from chackra_web.user.infraestructure.converter import factory as user_converter_factory

from chackra_web.user.infraestructure import migrations as user_migrations, repositories as user_repositories
from chackra_web.auth.infraestructure import migrations as auth_migrations, repositories as auth_repositories
from chackra_web.food_track.infraestructure import (
    migrations as food_track_migrations,
    repositories as food_track_repositories
)
from chackra_web.shared.infraestructure import tasks as infraestructure_task

def get_configuration() -> shared_configuration.Configuration:
    factory_configuration = infraestructure_configuration_factory.ConfigurationFactory(env="DEV")
    return factory_configuration.build()


def get_web_app(
    configuration: shared_configuration.Configuration,
    dependencies: shared_extended_dependencies.ExtendedControllerDependencies,
    processers_handler: list[Callable] | None = None,
) -> domain_web_app.WebAppFactory:
    factory_web = infraestructure_web_factory.WebApplicationFactory()
    return factory_web.build(
        configuration=configuration,
        dependencies=dependencies,
        processers_handlers=processers_handler
    )


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


def get_repositories(
        dependencies: shared_dependencies.ControllerDependencies,
        factory_repositories: list[Type[shared_factory.RepositoryFactory]],
) -> shared_builder_repository.RepositoryStore:
    repository_store = shared_builder_repository.RepositoryStore(dependencies=dependencies)

    for factory_repository in factory_repositories:
        factory_store = factory_repository(dependencies=dependencies).build()
        repository_store += factory_store

    return repository_store


def inject_migrations(
        migration_handler: shared_migration.MigratorHandler,
        migrations: list[shared_migration.MigrateHandler],
):
    for migration in migrations:
        migration_handler.add_migration(migration)


def inject_controllers(
    web: domain_web_app.WebAppFactory,
    dependencies: shared_extended_dependencies.ExtendedControllerDependencies,
    controllers: list[Type[shared_controller.WebController]]
) -> None:
    for controller in controllers:
        web.add_controller(controller(dependencies=dependencies))


def build_converters_handlers(
    configuration: shared_configuration.Configuration,
) -> list[Callable]:
    converters_factories = [
        food_track_converter_factory.get_converter(configuration=configuration),
        user_converter_factory.get_converter(configuration=configuration),
    ]
    for converter_factory in converters_factories:
        for name, in_converter in converter_factory.items():
            infraestructure_handler_factory.inject_converters(name=name, converter=in_converter)

    handlers = infraestructure_handler_factory.get_handlers(configuration=configuration)
    return handlers


configuration = get_configuration()


def get_extended_dependences() -> shared_extended_dependencies.ExtendedControllerDependencies:
    log = get_logger(configuration)

    uow = get_uow(configuration, log)
    migration_handler = get_migration_handler(configuration, log, uow)

    migrations = []
    migrations.extend(user_migrations.get_migration_handlers(configuration=configuration))
    migrations.extend(auth_migrations.get_migration_handlers(configuration=configuration))
    migrations.extend(food_track_migrations.get_migration_handlers(configuration=configuration))

    inject_migrations(migration_handler=migration_handler, migrations=migrations)
    migration_handler.pre_execute()
    migration_handler.execute()

    dependencies = shared_dependencies.ControllerDependencies(
        configuration=configuration,
        uow=uow,
        logger=log,
    )

    repository_factories = [
        user_repositories.UserRepositoryFactory,
        auth_repositories.AuthRepositoryFactory,
        food_track_repositories.InventoryRepositoryFactory,
    ]
    repositories_store = get_repositories(dependencies=dependencies, factory_repositories=repository_factories)


    specification_builder = infraestructure_specification_factory.SpecificationsGenericsFactory().build(
        configuration=configuration,
        logger=log
    )

    to_specification_builder = infraestructure_convertion_specification_factory.ToSpecificationFactory().build(
        configuration=configuration,
        specification_builder=specification_builder,
        logger=log
    )

    pagination_builder = infraestructure_pagination_factory.PaginationFactory().build(configuration=configuration)

    to_conversation_handler = infraestructure_convertion_pagination_factory.ToConvertionFactory().build(
        configuration=configuration,
        pagination_builder=pagination_builder,
        logger=log
    )

    extended_dependencies = shared_extended_dependencies.ExtendedControllerDependencies.from_dependencies(
        controller_dependencies=dependencies,
        repository_store=repositories_store,
        specification_builder=specification_builder,
        paginator_builder=pagination_builder,
        to_specification_builder=to_specification_builder,
        to_pagination_builder=to_conversation_handler,
    )

    task_queue_port = infraestructure_task.get_task_port(configuration=configuration, dependencies=extended_dependencies)

    extended_dependencies.inject_task_queue_adapter(task_queue_port)

    return extended_dependencies
