import pydantic

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger

from chackra_web.food_track.domain.models import inventory as model_inventory, exceptions as inventory_exceptions
from chackra_web.food_track.domain.models import inventory as domain_inventory, repositories as inventory_repositories

from chackra_web.shared.domain.model.food_track import inventory_id as shared_inventory_id
from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies

from chackra_web.food_track.domain.services.inventory import delete as inventory_delete


class DeleteInventoryItemDTO(pydantic.BaseModel):
    id: str


class DeleteInventoryItemCommand:
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

    def execute(self, delete_request: DeleteInventoryItemDTO) -> None:
        try:
            inventory_delete.delete_inventory_item(
                id=shared_inventory_id.InventoryID(value=delete_request.id),
                inventory_repository=self.inventory_repository
            )
        except inventory_exceptions.InventoryItemHasAlreadyDeletedException:
            self.logger.info("Inventory item '{}' has already been deleted".format(delete_request.id))
            return None