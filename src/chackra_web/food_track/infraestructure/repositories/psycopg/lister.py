from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.infraestructure.repositories.psycopg import (
    generics as psycopg_generics
)
from chackra_web.food_track.domain.models import inventory as domain_inventory, to_buy as domain_to_buy
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


class PsycopgToBuyListerRepository(psycopg_generics.PsycopgGenericLister[domain_to_buy.FoodTrackToBuy]):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_food_track_commons.TO_BUY_LIST_NAME,
            uow=uow,
            serializer=psycopg_food_track_commons.ToBuyListSerializer(),
            model_class=domain_to_buy.FoodTrackToBuy,
            default_filters="active = true",
        )


class PsycopgToBuyItemListerRepository(psycopg_generics.PsycopgGenericLister[domain_to_buy.FoodTrackToBuyItem]):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_food_track_commons.TO_BUY_ITEM_NAME,
            uow=uow,
            serializer=psycopg_food_track_commons.ToBuyItemSerializer(),
            model_class=domain_to_buy.FoodTrackToBuyItem,
            default_filters="active = true",
        )
