import pydantic

from chackra_web.food_track.domain.models import (
    inventory as domain_inventory,
    exceptions as domain_exceptions
)

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.quantity import quantity as shared_quantity
from chackra_web.shared.domain.model.food_track import inventory_id as shared_inventory_id, to_buy as shared_to_buy_id

from chackra_web.food_track.application.inventory import get_by_id as application_inventory_get_by_id
from chackra_web.food_track.application.to_buy import create as application_to_buy_create


class AddingItemIntoToBuyListDTO(pydantic.BaseModel):
    to_buy_id: str
    inventory_id: str
    comment: str
    quantity: shared_quantity.Quantity


class AddingItemIntoToBuyListCommand:
    dependencies: domain_dependencies.ExtendedControllerDependencies

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies):
        self.dependencies = dependencies

    def execute(self, adding_item_into_to_buy_list_dto: AddingItemIntoToBuyListDTO) -> None:
        to_buy_id, inventory_id = self._add_ids(adding_item_into_to_buy_list_dto)

        inventory_item = self._get_inventory_by_id(inventory_id)
        if not inventory_item:
            raise domain_exceptions.InventoryItemNotExistsException()

        name_inventory_item = inventory_item.name

        self._create_into_to_buy_item(
            name=name_inventory_item,
            to_buy_list_id=to_buy_id,
            inventory_id=inventory_id,
            adding_item_into_to_buy_list_dto=adding_item_into_to_buy_list_dto,
        )

    def _add_ids(self, adding_item_into_to_buy_list_dto: AddingItemIntoToBuyListDTO) -> tuple[
        shared_to_buy_id.FoodTrackToBuyId,
        shared_inventory_id.InventoryID
    ]:
        return (
            shared_to_buy_id.FoodTrackToBuyId(value=adding_item_into_to_buy_list_dto.to_buy_id),
            shared_inventory_id.InventoryID(value=adding_item_into_to_buy_list_dto.inventory_id)
        )

    def _get_inventory_by_id(
            self,
            inventory_id: shared_inventory_id.InventoryID
    ) -> domain_inventory.InventoryItem | None:
        return application_inventory_get_by_id.GetByIdInventoryItemCommand(dependencies=self.dependencies).execute(
            application_inventory_get_by_id.GetByIdInventoryIdDTO(id=inventory_id.value)
        )

    def _create_into_to_buy_item(
            self,
            name: str,
            adding_item_into_to_buy_list_dto: AddingItemIntoToBuyListDTO,
            to_buy_list_id: shared_to_buy_id.FoodTrackToBuyId,
            inventory_id: shared_inventory_id.InventoryID
    ) -> None:
        application_to_buy_create.CreateItemIntoToBuyListCommand(dependencies=self.dependencies).execute(
            create_to_buy_item_dto=application_to_buy_create.CreateToBuyItemDTO(
                name=name,
                comment=adding_item_into_to_buy_list_dto.comment,
                to_buy_list=to_buy_list_id,
                inventory_id=inventory_id,
                quantity=adding_item_into_to_buy_list_dto.quantity
            )
        )
