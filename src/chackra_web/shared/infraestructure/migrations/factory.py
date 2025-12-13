from typing import Type, TypeVar

from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.migration import migration as shared_migration
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.uow import uow as shared_uow

from chackra_web.shared.infraestructure.migrations.psycopg import handler as handler_psycopg


T = TypeVar("T", bound=shared_migration.MigratorHandler)


migration_handlers: dict[str, Type[T]] = {
    "psycopg":  handler_psycopg.PsycopgMigrationHandler,
}


class MigrationFactory:
    name_configuration_attribute: str = "migration_adapter"

    def build(
            self,
            configuration: shared_configuration.Configuration,
            logger: shared_logger.LogAdapter,
            uow: shared_uow.UOW
    ) -> T:
        logging_factory_value = getattr(configuration, self.name_configuration_attribute, "psycopg").lower()
        handler = migration_handlers.get(logging_factory_value)

        return handler(configuration=configuration, logger=logger, uow=uow)
