from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.food_track import inventory_id as shared_inventory_id, to_buy as shared_to_buy_id
from chackra_web.shared.infraestructure.repositories.psycopg import generics as psycopg_generics

from chackra_web.food_track.domain.models import inventory as domain_inventory_items, to_buy as domain_to_buy

from chackra_web.food_track.infraestructure.repositories.psycopg import commons as psycopg_food_track_commons


class PsycopgInventoryItemUpdaterRepository(
    psycopg_generics.PsycopgGenericUpdaterRepository[
        domain_inventory_items.InventoryItem,
        shared_inventory_id.InventoryID
    ]
):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_food_track_commons.TABLE_NAME,
            uow=uow,
            model_class=domain_inventory_items.InventoryItem,
            serializer=psycopg_food_track_commons.InventorySerializer(),
        )


class PsycopgToBuyListUpdaterRepository(
    psycopg_generics.PsycopgGenericUpdaterRepository[
        domain_to_buy.FoodTrackToBuy,
        shared_to_buy_id.FoodTrackToBuyId,
    ]
):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_food_track_commons.TO_BUY_LIST_NAME,
            uow=uow,
            model_class=domain_to_buy.FoodTrackToBuy,
            serializer=psycopg_food_track_commons.ToBuyListSerializer(),
        )
