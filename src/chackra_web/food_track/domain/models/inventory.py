import pydantic
import datetime
import uuid

from chackra_web.shared.domain.model.food_track import inventory_id as shared_inventory_id
from chackra_web.shared.domain.model.quantity import quantity as shared_quantity


class BaseInventoryDTO(pydantic.BaseModel):
    name: str
    quantity: shared_quantity.Quantity


class InventoryItem(pydantic.BaseModel):
    id: shared_inventory_id.InventoryID
    name: str
    quantity: shared_quantity.Quantity
    is_sold_out: bool = False

    active: bool = True
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()
    deleted_at: datetime.datetime | None = None

    @staticmethod
    def create(inv_data: BaseInventoryDTO) -> "InventoryItem":
        return InventoryItem(
            id=shared_inventory_id.InventoryID(value=str(uuid.uuid4())),
            name=inv_data.name.lower(),
            quantity=inv_data.quantity,
        )

    def model_dump(self, *args, **kwargs) -> dict:
        value = super().model_dump(*args, **kwargs)
        print("my value - ", value)
        if "quantity" in value:
            value["quantity_measure_unit"] = value["quantity"]["measure_unit"]
            value["quantity_value"] = value["quantity"]["value"]
            value.pop("quantity")
        return value
