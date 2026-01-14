import dataclasses

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.pagination import pagination as shared_pagination
from chackra_web.food_track.domain.models import inventory as model_inventory
from chackra_web.food_track.domain.models import repositories as inventory_repositories
from chackra_web.shared.domain.model.food_track import inventory_id as shared_inventory_id

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.specifications import builder as shared_specification_builder
from chackra_web.shared.domain.model.pagination import builder as shared_pagination_builder


@dataclasses.dataclass
class ListInventoryItemMatchingDTO:
    pagination: shared_pagination.Pagination


@dataclasses.dataclass
class SearchInventoryItemMatchingDTO:
    pagination: shared_pagination.Pagination


class ListInventoryItemCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    inventory_repository:  inventory_repositories.InventoryRepository[
        model_inventory.InventoryItem,
        shared_inventory_id.InventoryID
    ]
    specification_builder: shared_specification_builder.SpecificationBuilder

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger

        self.inventory_repository = dependencies.repository_store.build(
            inventory_repositories.InventoryRepository[
                model_inventory.InventoryItem,
                shared_inventory_id.InventoryID
            ]
        )
        self.specification_builder = dependencies.specification_builder

    def execute(self, list_inventory_item_matching_dto: ListInventoryItemMatchingDTO) -> shared_pagination.Paginator:
        return self.inventory_repository.matching(list_inventory_item_matching_dto.pagination)


class SearchInventoryItemCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    inventory_repository:  inventory_repositories.InventoryRepository[
        model_inventory.InventoryItem,
        shared_inventory_id.InventoryID
    ]
    specification_builder: shared_specification_builder.SpecificationBuilder
    paginator_builder: shared_pagination_builder.PaginationBuilder

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies) -> None:
        self.uow = dependencies.uow
        self.logger = dependencies.logger

        self.inventory_repository = dependencies.repository_store.build(
            inventory_repositories.InventoryRepository[
                model_inventory.InventoryItem,
                shared_inventory_id.InventoryID
            ]
        )
        self.specification_builder = dependencies.specification_builder
        self.paginator_builder = dependencies.paginator_builder

    def execute(self, list_inventory_item_matching_dto: SearchInventoryItemMatchingDTO) -> shared_pagination.Paginator:
        if filters := list_inventory_item_matching_dto.pagination.filters:
            if search_specification := filters.find_by_attribute("search"):
                name_like_specification = self.specification_builder.build(
                    "name",
                    "ilike",
                    search_specification.value,
                )
                filtered_or_like = (
                        name_like_specification
                )
                list_inventory_item_matching_dto.pagination.filters = (
                    list_inventory_item_matching_dto.pagination.filters.find_and_replace_by_attribute(
                        "search",
                        filtered_or_like
                    )
                )

        return self.inventory_repository.matching(list_inventory_item_matching_dto.pagination)
