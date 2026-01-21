from chackra_web.shared.domain.model.migration import migration as shared_migration

from chackra_web.user.infraestructure.migrations.psycopg import (
    migration_1_create_user_table,
    migration_2_create_additional_information_user,
)


migrations: list[shared_migration.MigrateHandler] = [
    shared_migration.MigrateHandler(
        module="user",
        name="migration_1_create_user_table",
        migrator=migration_1_create_user_table.migrator,
    ),
    shared_migration.MigrateHandler(
        module="user",
        name="migration_2_create_additional_information_user",
        migrator=migration_2_create_additional_information_user.migrator,
    ),
]