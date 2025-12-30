from chackra_web.shared.domain.model.migration import migration as migrator_model


migrator_script = """
CREATE TABLE IF NOT EXISTS tbl_inventory(
    id VARCHAR(50) PRIMARY KEY NOT NULL,
    name VARCHAR(120) NOT NULL,
    quantity_measure_unit VARCHAR(10) NOT NULL,
    quantity_value FLOAT NOT NULL,
    is_sold_out BOOL NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP NULL
);
"""

rollback_script = """
DROP TABLE IF EXISTS tbl_inventory;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
