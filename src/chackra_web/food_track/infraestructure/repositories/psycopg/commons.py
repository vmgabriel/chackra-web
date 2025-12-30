from typing import Any

from chackra_web.shared.infraestructure.repositories.psycopg import commons as psycopg_commons


TABLE_NAME: str = "tbl_inventory"


class InventorySerializer(psycopg_commons.BasicTypeSerializer):
    def from_primitive(self, value: Any, model_class: type[psycopg_commons.T]) -> psycopg_commons.T | None:
        if value is None:
            return None
        if isinstance(value, dict):
            value["quantity"] = {
                "value": value["quantity_value"],
                "measure_unit": value["quantity_measure_unit"],
            }
            value.pop("quantity_value")
            value.pop("quantity_measure_unit")
            return model_class(**value)
        raise ValueError(f"Cannot convert {type(value)} to {model_class}")