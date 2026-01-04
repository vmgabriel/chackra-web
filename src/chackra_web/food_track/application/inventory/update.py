import pydantic

from chackra_web.food_track.domain.models import (
    inventory as model_inventory,
    exceptions as inventory_exceptions,
    repositories as inventory_repositories
)

from chackra_web.shared.domain.model.food_track import inventory_id as shared_inventory_id
from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.quantity import quantity as shared_quantity
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger

from chackra_web.food_track.domain.services.inventory import update as update_inventory_item_service


class UpdateInventoryItemRequestDTO(pydantic.BaseModel):
    id: str
    name: str
    quantity_value: float
    quantity_measure_unit: shared_quantity.MeasureUnitType
    is_sold_out: bool


class UpdateInventoryItemCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    inventory_repository:  inventory_repositories.InventoryRepository[
        model_inventory.InventoryItem,
        shared_inventory_id.InventoryID
    ]

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies):
        self.uow = dependencies.uow
        self.logger = dependencies.logger
        self.inventory_repository = dependencies.repository_store.build(
            inventory_repositories.InventoryRepository[model_inventory.InventoryItem, shared_inventory_id.InventoryID]
        )

    def execute(self, update_inventory_item_dto: UpdateInventoryItemRequestDTO) -> model_inventory.InventoryItem:
        inventory_item_id = shared_inventory_id.InventoryID(value=update_inventory_item_dto.id)
        changes = model_inventory.UpdateInventoryItemDTO(
            name=update_inventory_item_dto.name,
            quantity=shared_quantity.Quantity(
                value=update_inventory_item_dto.quantity_value,
                measure_unit=update_inventory_item_dto.quantity_measure_unit,
            ),
            is_sold_out=update_inventory_item_dto.is_sold_out,
        )

        return update_inventory_item_service.update_inventory_item(
            id=inventory_item_id,
            changes=changes,
            inventory_repository=self.inventory_repository
        )


