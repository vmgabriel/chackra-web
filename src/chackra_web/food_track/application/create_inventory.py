import pydantic

from chackra_web.food_track.domain.models import inventory as model_inventory, exceptions as inventory_exceptions
from chackra_web.food_track.domain.models import inventory as domain_inventory, repositories as inventory_repositories

from chackra_web.shared.domain.model.food_track import inventory_id as shared_inventory_id
from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.quantity import quantity as shared_quantity
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger


class CreateInventoryDTO(pydantic.BaseModel):
    name: str
    quantity: shared_quantity.Quantity


class CreateInventoryCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    inventory_repository:  inventory_repositories.InventoryRepository[model_inventory.InventoryItem, shared_inventory_id.InventoryID]

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies):
        self.uow = dependencies.uow
        self.logger = dependencies.logger
        self.inventory_repository = dependencies.repository_store.build(
            inventory_repositories.InventoryRepository[model_inventory.InventoryItem, shared_inventory_id.InventoryID]
        )

    def execute(self, create_inventory_dto: CreateInventoryDTO) -> domain_inventory.InventoryItem:
        inventory_created = domain_inventory.InventoryItem.create(
            inv_data=domain_inventory.BaseInventoryDTO(
                name=create_inventory_dto.name,
                quantity=create_inventory_dto.quantity,
            )
        )

        inventory_exists = self.inventory_repository.find_by_name(name=create_inventory_dto.name.lower())
        print("inventory_exists - ", inventory_exists)
        if inventory_exists:
            raise inventory_exceptions.InventoryItemExistsException()

        return self.inventory_repository.create(entity=inventory_created)

