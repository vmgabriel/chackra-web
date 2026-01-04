from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.infraestructure.repositories.psycopg import (
    generics as psycopg_generics
)
from chackra_web.food_track.domain.models import inventory as domain_inventory
from chackra_web.food_track.infraestructure.repositories.psycopg import commons as psycopg_food_track_commons


class PsycopgInventoryItemListerRepository(psycopg_generics.PsycopgGenericLister[domain_inventory.InventoryItem]):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_food_track_commons.TABLE_NAME,
            uow=uow,
            serializer=psycopg_food_track_commons.InventorySerializer(),
            model_class=domain_inventory.InventoryItem,
            default_filters="active = true",
        )
