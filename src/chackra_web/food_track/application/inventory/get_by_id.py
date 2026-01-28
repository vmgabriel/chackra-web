import pydantic

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger

from chackra_web.food_track.domain.models import (
    inventory as model_inventory,
    exceptions as inventory_exceptions,
    repositories as inventory_repositories
)

from chackra_web.shared.domain.model.food_track import inventory_id as shared_inventory_id
from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies

from chackra_web.food_track.domain.services.inventory import get_by_id as inventory_get_by_id


class GetByIdInventoryIdDTO(pydantic.BaseModel):
    id: str


class GetByIdInventoryItemCommand:
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

    def execute(self, get_by_id: GetByIdInventoryIdDTO) -> model_inventory.InventoryItem:
        inventory_item_id = shared_inventory_id.InventoryID(value=get_by_id.id)
        inventory_item = inventory_get_by_id.get_by_id(
            id=inventory_item_id,
            inventory_repository=self.inventory_repository
        )
        if not inventory_item:
            raise inventory_exceptions.InventoryItemNotExistsException()

        return inventory_item
