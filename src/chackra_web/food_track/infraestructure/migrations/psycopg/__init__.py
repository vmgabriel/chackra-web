from chackra_web.shared.domain.model.migration import migration as shared_migration

from chackra_web.food_track.infraestructure.migrations.psycopg import migration_1_create_table_inventory


migrations: list[shared_migration.MigrateHandler] = [
    shared_migration.MigrateHandler(
        module="food_track",
        name="migration_1_create_table_inventory",
        migrator=migration_1_create_table_inventory.migrator,
    ),
]