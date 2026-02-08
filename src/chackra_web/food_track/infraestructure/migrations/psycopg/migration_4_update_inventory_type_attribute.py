from chackra_web.shared.domain.model.migration import migration as migrator_model


migrator_script = """
ALTER TABLE tbl_inventory
ADD type VARCHAR(50)
;

UPDATE tbl_inventory SET type = 'food'
;
    
ALTER TABLE tbl_inventory
ALTER COLUMN type SET NOT NULL
;
"""

rollback_script = """
ALTER TABLE tbl_inventory
ALTER COLUMN type DROP NOT NULL
;

ALTER TABLE tbl_inventory
DROP COLUMN IF EXISTS type
;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
