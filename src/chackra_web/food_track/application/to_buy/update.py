import pydantic

from chackra_web.food_track.domain.models import (
    to_buy as model_to_buy,
    repositories as food_track_repositories,
    exceptions as food_tracking_exceptions
)

from chackra_web.shared.domain.model.food_track import (
    to_buy as shared_to_buy_id,
    inventory_id as shared_inventory_id
)
from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.quantity import quantity as shared_quantity

from chackra_web.food_track.domain.services.to_buy import update as update_to_buy

from chackra_web.food_track.application.inventory import get_by_id as inventory_get_by_id


class UpdateToBuyListRequestDTO(pydantic.BaseModel):
    id: st
    title: str
    description: str
    is_bought: bool


class UpdateToBuyListCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    to_buy_list_repository:  food_track_repositories.ToBuyListRepository[
        model_to_buy.FoodTrackToBuy,
        shared_to_buy_id.FoodTrackToBuyId,
    ]

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies):
        self.uow = dependencies.uow
        self.logger = dependencies.logger
        self.to_buy_list_repository = dependencies.repository_store.build(
            food_track_repositories.ToBuyListRepository[
                model_to_buy.FoodTrackToBuy,
                shared_to_buy_id.FoodTrackToBuyId,
            ]
        )

    def execute(self, update_dto: UpdateToBuyListRequestDTO) -> model_to_buy.FoodTrackToBuy:
        to_buy_list_id = shared_to_buy_id.FoodTrackToBuyId(value=update_dto.id)
        changes = model_to_buy.UpdateFoodTrackToBuyDTO(
            title=update_dto.title,
            description=update_dto.description,
            is_bought=update_dto.is_bought,
        )

        return update_to_buy.update_to_buy_list(
            id=to_buy_list_id,
            changes=changes,
            to_buy_list_repository=self.to_buy_list_repository
        )


class UpdateToBuyItemRequestDTO(pydantic.BaseModel):
    to_buy_item_id: str
    to_buy_id: str
    inventory_id: str
    comment: str
    quantity: shared_quantity.Quantity


class UpdateToBuyItemCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    to_buy_items_repository: food_track_repositories.ToBuyItemListRepository[
        model_to_buy.FoodTrackToBuyItem,
        shared_to_buy_id.FoodTrackItemToBuyId,
    ]
    dependencies: domain_dependencies.ExtendedControllerDependencies

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies):
        self.uow = dependencies.uow
        self.logger = dependencies.logger
        self.to_buy_items_repository = dependencies.repository_store.build(
            food_track_repositories.ToBuyItemListRepository[
                model_to_buy.FoodTrackToBuyItem,
                shared_to_buy_id.FoodTrackItemToBuyId,
            ]
        )
        self.dependencies = dependencies


    def execute(self, update_dto: UpdateToBuyItemRequestDTO) -> model_to_buy.FoodTrackToBuyItem:
        to_buy_item_id = shared_to_buy_id.FoodTrackItemToBuyId(value=update_dto.to_buy_item_id)

        inventory_item = inventory_get_by_id.GetByIdInventoryItemCommand(
            self.dependencies
        ).execute(inventory_get_by_id.GetByIdInventoryIdDTO(id=update_dto.inventory_id))
        if not inventory_item:
            raise food_tracking_exceptions.InventoryItemNotExistsException()

        changes = model_to_buy.UpdateFoodTrackToBuyItemDTO(
            name=inventory_item.name,
            comment=update_dto.comment,
            quantity=update_dto.quantity,
            to_buy_id=shared_to_buy_id.FoodTrackToBuyId(value=update_dto.to_buy_id),
            inventory_id=shared_inventory_id.InventoryID(value=update_dto.inventory_id),
        )

        return update_to_buy.update_to_buy_item(
            id=to_buy_item_id,
            changes=changes,
            to_buy_items_repository=self.to_buy_items_repository,
        )
