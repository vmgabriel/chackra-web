from chackra_web.shared.domain.model.migration import migration as shared_migration

from chackra_web.user.infraestructure.migrations.psycopg import migration_1_create_user_table

migrations: list[shared_migration.MigrateHandler] = [
    shared_migration.MigrateHandler(
        name="migration_1_create_user_table",
        migrator=migration_1_create_user_table.migrator,
    ),
]