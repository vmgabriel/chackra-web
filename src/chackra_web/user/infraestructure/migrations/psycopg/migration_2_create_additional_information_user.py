from chackra_web.shared.domain.model.migration import migration as migrator_model


migrator_script = """
CREATE TABLE IF NOT EXISTS tbl_additional_information_user (
    id VARCHAR(50) PRIMARY KEY NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    genre VARCHAR(20) NOT NULL,
    country VARCHAR(50) NOT NULL,
    height NUMERIC(5, 2) NOT NULL,
    weight NUMERIC(5, 2) NOT NULL,
    profession VARCHAR(120) NOT NULL,
    work_schedule JSONB NOT NULL,
    health_difficulties TEXT NOT NULL,
    allergenic_products TEXT NOT NULL,
    lifestyle VARCHAR(30) NOT NULL,
    with_oven BOOLEAN NOT NULL,
    foods VARCHAR(100) NOT NULL,
    sleep_phase JSONB NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    deleted_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES tbl_user(id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""

rollback_script = """
DROP TABLE IF EXISTS tbl_additional_information_user;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
