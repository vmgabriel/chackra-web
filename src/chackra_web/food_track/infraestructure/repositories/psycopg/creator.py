from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.infraestructure.repositories.psycopg import generics as psycopg_generics
from chackra_web.food_track.domain.models import inventory as domain_inventory, to_buy as domain_to_buy
from chackra_web.food_track.infraestructure.repositories.psycopg import commons as psycopg_inventory_commons


class PsycopgInventoryCreatorRepository(psycopg_generics.PsycopgGenericCreator[domain_inventory.InventoryItem]):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_inventory_commons.TABLE_NAME,
            uow=uow,
            serializer=psycopg_inventory_commons.InventorySerializer()
        )


class PsycopgToBuyCreatorRepository(psycopg_generics.PsycopgGenericCreator[domain_to_buy.FoodTrackToBuy]):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_inventory_commons.TO_BUY_LIST_NAME,
            uow=uow,
            serializer=psycopg_inventory_commons.ToBuyListSerializer(),
        )


class PsycopgToBuyItemCreatorRepository(psycopg_generics.PsycopgGenericCreator[domain_to_buy.FoodTrackToBuyItem]):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_inventory_commons.TO_BUY_ITEM_NAME,
            uow=uow,
            serializer=psycopg_inventory_commons.ToBuyItemSerializer(),
        )
