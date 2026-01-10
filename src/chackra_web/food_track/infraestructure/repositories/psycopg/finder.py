from typing import Type

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.food_track.domain.models import (
    inventory as domain_inventory,
    to_buy as domain_to_buy,
    behavior as inventory_behavior
)
from chackra_web.shared.domain.model.food_track import inventory_id as shared_inventory_id
from chackra_web.food_track.infraestructure.repositories.psycopg import commons as psycopg_inventory_commons
from chackra_web.shared.infraestructure.repositories.psycopg import (
    commons as psycopg_commons
)

from chackra_web.shared.infraestructure.repositories.psycopg import generics as psycopg_generics


class PsycopgBaseInventoryFinderRepository(
    shared_behavior.FinderBehavior[shared_behavior.M, shared_behavior.ID],
    inventory_behavior.NameFinderBehavior[shared_behavior.M],
):
    table_name: str
    uow: shared_uow.UOW
    serializer: psycopg_commons.SafeSerializer
    model_class: type[domain_inventory.InventoryItem] = domain_inventory.InventoryItem

    FIND_BY_ID_QUERY = """
    SELECT *
    FROM {table_name}
    WHERE id = %s AND active = true;
    """
    FIND_BY_NAME_QUERY = "SELECT * FROM {table_name} WHERE name = %s AND active = true;"

    def __init__(
            self,
            table_name: str,
            uow: shared_uow.UOW,
            model_class: Type[shared_behavior.M],
            serializer: psycopg_commons.SafeSerializer = psycopg_commons.BasicTypeSerializer(),
    ) -> None:
        super().__init__(uow)
        self.table_name = table_name
        self.uow = uow
        self.serializer = serializer
        self.model_class = model_class

    def find_by_id(self, id: shared_behavior.ID) -> shared_behavior.M | None:
        query = self.FIND_BY_ID_QUERY.format(table_name=self.table_name)
        return psycopg_commons.execute_query(
            query=query,
            params=(id.value,),
            uow=self.uow,
            model_class=self.model_class,
            serializer=self.serializer,
        )

    def find_by_name(self, name: str) -> shared_behavior.M | None:
        query = self.FIND_BY_NAME_QUERY.format(table_name=self.table_name)
        return psycopg_commons.execute_query(
            query=query,
            params=(name,),
            uow=self.uow,
            model_class=self.model_class,
            serializer=self.serializer,
        )



class PsycopgInventoryFinderRepository(
    PsycopgBaseInventoryFinderRepository[domain_inventory.InventoryItem, shared_inventory_id.InventoryID]
):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_inventory_commons.TABLE_NAME,
            uow=uow,
            model_class=domain_inventory.InventoryItem,
            serializer=psycopg_inventory_commons.InventorySerializer()
        )


class PsycopgToBuyListFinderRepository(
    psycopg_generics.PsycopgGenericFinder[shared_behavior.M, shared_behavior.ID],
):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_inventory_commons.TO_BUY_LIST_NAME,
            uow=uow,
            model_class=domain_to_buy.FoodTrackToBuy,
            serializer=psycopg_inventory_commons.ToBuyListSerializer()
        )


class PsycopgToBuyItemFinderRepository(
    psycopg_generics.PsycopgGenericFinder[shared_behavior.M, shared_behavior.ID],
):
    def __init__(self, uow: shared_uow.UOW) -> None:
        super().__init__(
            table_name=psycopg_inventory_commons.TO_BUY_ITEM_NAME,
            uow=uow,
            model_class=domain_to_buy.FoodTrackToBuyItem,
            serializer=psycopg_inventory_commons.ToBuyItemSerializer(),
        )
