import pydantic
import datetime
import uuid

from chackra_web.shared.domain.model.food_track import inventory_id as shared_inventory_id
from chackra_web.shared.domain.model.quantity import quantity as shared_quantity
from chackra_web.food_track.domain.models import exceptions as food_track_exceptions


class BaseInventoryDTO(pydantic.BaseModel):
    name: str
    quantity: shared_quantity.Quantity


class UpdateInventoryItemDTO(pydantic.BaseModel):
    name: str
    quantity: shared_quantity.Quantity
    is_sold_out: bool


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

    def update(self, changes: UpdateInventoryItemDTO) -> "InventoryItem":
        self.name = changes.name
        self.quantity = changes.quantity
        self.is_sold_out = changes.is_sold_out
        self.updated_at = datetime.datetime.now()
        return self

    def delete(self) -> None:
        if not self.active:
            raise food_track_exceptions.InventoryItemHasAlreadyDeletedException()
        self.deleted_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.active = False

    def model_dump(self, *args, **kwargs) -> dict:
        value = super().model_dump(*args, **kwargs)
        if "quantity" in value:
            value["quantity_measure_unit"] = value["quantity"]["measure_unit"]
            value["quantity_value"] = value["quantity"]["value"]
            value.pop("quantity")
        return value
