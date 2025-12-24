from chackra_web.shared.domain.model.migration import migration as shared_migration

from chackra_web.auth.infraestructure.migrations.psycopg import migration_1_create_table_auth


migrations: list[shared_migration.MigrateHandler] = [
    shared_migration.MigrateHandler(
        module="auth",
        name="migration_1_create_table_auth",
        migrator=migration_1_create_table_auth.migrator,
    ),
]