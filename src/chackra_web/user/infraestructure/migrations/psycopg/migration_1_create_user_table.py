from chackra_web.shared.domain.model.migration import migration as migrator_model


migrator_script = """
CREATE TABLE IF NOT EXISTS tbl_user(
    id VARCHAR(50) PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP NULL
);
"""

rollback_script = """
DROP TABLE IF EXISTS tbl_user;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
