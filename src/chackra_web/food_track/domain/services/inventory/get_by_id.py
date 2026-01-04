from chackra_web.shared.domain.model.food_track import inventory_id as shared_inventory_id
from chackra_web.food_track.domain.models import inventory as model_inventory
from chackra_web.food_track.domain.models import repositories as inventory_repositories


def get_by_id(
    id: shared_inventory_id.InventoryID,
    inventory_repository: inventory_repositories.InventoryRepository[
        model_inventory.InventoryItem,
        shared_inventory_id.InventoryID
    ]
) -> model_inventory.InventoryItem | None:
    return inventory_repository.find_by_id(id)