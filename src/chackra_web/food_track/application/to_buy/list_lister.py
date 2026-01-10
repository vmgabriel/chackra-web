import dataclasses

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.pagination import pagination as shared_pagination
from chackra_web.food_track.domain.models import to_buy as model_to_buy
from chackra_web.food_track.domain.models import repositories as inventory_repositories
from chackra_web.shared.domain.model.food_track import to_buy as shared_to_buy_id

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.specifications import builder as shared_specification_builder


@dataclasses.dataclass
class ListToBuyMatchingDTO:
    pagination: shared_pagination.Pagination


@dataclasses.dataclass
class ListToBuyItemsMatchingDTO:
    pagination: shared_pagination.Pagination


class ListToBuyCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    to_buy_list_repository:  inventory_repositories.ToBuyListRepository[
        model_to_buy.FoodTrackToBuy,
        shared_to_buy_id.FoodTrackToBuyId,
    ]
    specification_builder: shared_specification_builder.SpecificationBuilder

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger

        self.to_buy_list_repository = dependencies.repository_store.build(
            inventory_repositories.ToBuyListRepository[
                model_to_buy.FoodTrackToBuy,
                shared_to_buy_id.FoodTrackToBuyId,
            ]
        )
        self.specification_builder = dependencies.specification_builder

    def execute(self, list_inventory_item_matching_dto: ListToBuyMatchingDTO) -> shared_pagination.Paginator:
        return self.to_buy_list_repository.matching(list_inventory_item_matching_dto.pagination)



class ToBuyItemListCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    to_buy_items_repository:  inventory_repositories.ToBuyItemListRepository[
        model_to_buy.FoodTrackToBuyItem,
        shared_to_buy_id.FoodTrackItemToBuyId,
    ]
    specification_builder: shared_specification_builder.SpecificationBuilder

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger

        self.to_buy_items_repository = dependencies.repository_store.build(
            inventory_repositories.ToBuyItemListRepository[
                model_to_buy.FoodTrackToBuyItem,
                shared_to_buy_id.FoodTrackItemToBuyId,
            ]
        )
        self.specification_builder = dependencies.specification_builder

    def execute(self, list_to_buy_items_matching_dto: ListToBuyItemsMatchingDTO) -> shared_pagination.Paginator:
        return self.to_buy_items_repository.matching(list_to_buy_items_matching_dto.pagination)
