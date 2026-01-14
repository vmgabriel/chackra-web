from chackra_web.shared.domain.model.migration import migration as migrator_model


migrator_script = """
ALTER TABLE tbl_to_buy_item
ADD inventory_id VARCHAR(50)
;

ALTER TABLE tbl_to_buy_item
ADD CONSTRAINT fk_inventory_to_buy_item
FOREIGN KEY (inventory_id) REFERENCES tbl_inventory(id)
;

UPDATE tbl_to_buy_item SET inventory_id = (SELECT id FROM tbl_inventory LIMIT 1)
;
    
ALTER TABLE tbl_to_buy_item
ALTER COLUMN inventory_id SET NOT NULL
;
"""

rollback_script = """
ALTER TABLE tbl_to_buy_item
ALTER COLUMN inventory_id DROP NOT NULL
;

ALTER TABLE tbl_to_buy_item
DROP CONSTRAINT IF EXISTS fk_inventory_to_buy_item
;

ALTER TABLE tbl_to_buy_item
DROP COLUMN IF EXISTS inventory_id
;
"""


migrator = migrator_model.Migrator(
    up=migrator_script,
    rollback=rollback_script,
)
