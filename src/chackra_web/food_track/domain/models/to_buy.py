import pydantic
import datetime
import uuid

from chackra_web.shared.domain.model.food_track import to_buy as to_buy_id, inventory_id as shared_inventory_id
from chackra_web.shared.domain.model.quantity import quantity as shared_quantity

from chackra_web.food_track.domain.models import exceptions as food_track_exceptions


class CreateFoodTrackToBuyItemDTO(pydantic.BaseModel):
    name: str
    comment: str
    quantity: shared_quantity.Quantity
    to_buy_id: to_buy_id.FoodTrackToBuyId
    inventory_id: shared_inventory_id.InventoryID


class CreateFoodTrackToBuyDTO(pydantic.BaseModel):
    title: str
    description: str
    is_bought: bool


class UpdateFoodTrackToBuyDTO(pydantic.BaseModel):
    title: str
    description: str
    is_bought: bool


class FoodTrackToBuyItem(pydantic.BaseModel):
    id: to_buy_id.FoodTrackItemToBuyId
    to_buy_id: to_buy_id.FoodTrackToBuyId
    inventory_id: shared_inventory_id.InventoryID
    name: str
    quantity: shared_quantity.Quantity
    comment: str

    active: bool = True
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()
    deleted_at: datetime.datetime | None = None

    @staticmethod
    def create(create_dto: CreateFoodTrackToBuyItemDTO) -> "FoodTrackToBuyItem":
        return FoodTrackToBuyItem(
            id=to_buy_id.FoodTrackItemToBuyId(value=str(uuid.uuid4())),
            to_buy_id=create_dto.to_buy_id,
            inventory_id=create_dto.inventory_id,
            name=create_dto.name.lower(),
            quantity=create_dto.quantity,
            comment=create_dto.comment,
        )

    def __eq__(self, other: "FoodTrackToBuyItem") -> bool:
        if not isinstance(other, FoodTrackToBuyItem):
            return False
        return self.name == other.name or self.id == other.id

    def model_dump(self, *args, **kwargs) -> dict:
        value = super().model_dump(*args, **kwargs)
        if "quantity" in value:
            value["quantity_measure_unit"] = value["quantity"]["measure_unit"]
            value["quantity_value"] = value["quantity"]["value"]
            value.pop("quantity")
        return value


class FoodTrackToBuy(pydantic.BaseModel):
    id: to_buy_id.FoodTrackToBuyId
    title: str
    description: str
    is_bought: bool
    items: list[FoodTrackToBuyItem]

    active: bool = True
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()
    deleted_at: datetime.datetime | None = None

    @staticmethod
    def create(create_dto: CreateFoodTrackToBuyDTO) -> "FoodTrackToBuy":
        return FoodTrackToBuy(
            id=to_buy_id.FoodTrackToBuyId(value=str(uuid.uuid4())),
            title=create_dto.title,
            description=create_dto.description,
            is_bought=create_dto.is_bought,
            items=[]
        )

    def model_dump(self, *args, **kwargs) -> dict:
        value = super().model_dump(*args, **kwargs)
        if "items" in value:
            value.pop("items")
        return value

    def delete(self) -> None:
        self.updated_at = datetime.datetime.now()
        self.deleted_at = datetime.datetime.now()
        self.active = False

    def add_item(self, item: FoodTrackToBuyItem) -> None:
        if any(in_item == item for in_item in self.items):
            raise food_track_exceptions.ToBuyItemHasAlreadyRegisteredException()
        self.items.append(item)

    def update(self, to_update: UpdateFoodTrackToBuyDTO) -> "FoodTrackToBuy":
        self.is_bought = to_update.is_bought
        self.title = to_update.title
        self.description = to_update.description

        self.updated_at = datetime.datetime.now()
        return self
