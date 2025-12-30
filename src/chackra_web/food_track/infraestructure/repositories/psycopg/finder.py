from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.food_track.domain.models import inventory as domain_inventory
from chackra_web.shared.domain.model.food_track import inventory_id as shared_inventory_id
from chackra_web.food_track.infraestructure.repositories.psycopg import commons as psycopg_inventory_commons


class PsycopgInventoryFinderRepository(
    shared_behavior.FinderBehavior[domain_inventory.InventoryItem, shared_inventory_id.InventoryID]
):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_inventory_commons.TABLE_NAME,
            uow=uow,
            model_class=domain_inventory.InventoryItem,
            serializer=psycopg_inventory_commons
        )
