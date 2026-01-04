from chackra_web.shared.domain.model.migration import migration as migrator_model


migrator_script = """
CREATE TABLE IF NOT EXISTS tbl_to_buy(
    id VARCHAR(50) PRIMARY KEY NOT NULL,
    title VARCHAR(120) NOT NULL,
    description VARCHAR(240) NULL,
    is_bought BOOL NOT NULL DEFAULT FALSE,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS tbl_to_buy_item(
    id VARCHAR(50) PRIMARY KEY NOT NULL,
    to_buy_id VARCHAR(50) NOT NULL,
    name VARCHAR(120) NOT NULL,
    quantity_measure_unit VARCHAR(10) NOT NULL,
    quantity_value FLOAT NOT NULL,
    comment VARCHAR(240) NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (to_buy_id) REFERENCES tbl_to_buy(id) ON DELETE CASCADE ON UPDATE CASCADE 
);
"""

rollback_script = """
DROP TABLE IF EXISTS tbl_to_buy;

DROP TABLE IF EXISTS tbl_to_buy_item;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
