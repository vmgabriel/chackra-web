from chackra_web.shared.domain.model.migration import migration as shared_migration

from chackra_web.food_track.infraestructure.migrations.psycopg import (
    migration_1_create_table_inventory,
    migration_2_create_tables_for_to_buy,
)


migrations: list[shared_migration.MigrateHandler] = [
    shared_migration.MigrateHandler(
        module="food_track",
        name="migration_1_create_table_inventory",
        migrator=migration_1_create_table_inventory.migrator,
    ),
    shared_migration.MigrateHandler(
        module="food_track",
        name="migration_2_create_tables_for_to_buy",
        migrator=migration_2_create_tables_for_to_buy.migrator,
    ),
]