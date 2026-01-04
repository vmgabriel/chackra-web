from chackra_web.shared.domain.model.food_track import inventory_id as shared_inventory_id
from chackra_web.food_track.domain.models import (
    inventory as model_inventory,
    repositories as inventory_repositories,
    exceptions as inventory_exceptions
)

from chackra_web.food_track.domain.services.inventory import get_by_id as inventory_get_by_id


def delete_inventory_item(
    id: shared_inventory_id.InventoryID,
    inventory_repository: inventory_repositories.InventoryRepository[
        model_inventory.InventoryItem,
        shared_inventory_id.InventoryID
    ]
) -> None:
    inventory_item = inventory_get_by_id.get_by_id(id=id, inventory_repository=inventory_repository)
    if not inventory_item:
        raise inventory_exceptions.InventoryItemNotExistsException()

    inventory_item.delete()

    inventory_repository.update(id=id, entity=inventory_item)
