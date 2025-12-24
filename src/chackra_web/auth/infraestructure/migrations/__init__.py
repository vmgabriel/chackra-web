from typing import TypeVar, List

from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.migration import migration as shared_migration

from chackra_web.auth.infraestructure.migrations.psycopg import migrations as migrations_psycopg


T = TypeVar("T", bound=shared_migration.MigrateHandler)


migration_handlers: dict[str, List[T]] = {
    "psycopg":  migrations_psycopg,
}


def get_migration_handlers(configuration: shared_configuration.Configuration) -> List[T]:
    logging_factory_value = getattr(configuration, "migration_adapter", "psycopg").lower()
    return migration_handlers.get(logging_factory_value, [])