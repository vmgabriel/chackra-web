import pydantic

from chackra_web.food_track.domain.models import (
    to_buy as model_to_buy,
    repositories as inventory_repositories
)

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.food_track import to_buy as shared_to_buy_id, inventory_id as shared_inventory_id
from chackra_web.shared.domain.model.quantity import quantity as shared_quantity


class CreateToBuyListDTO(pydantic.BaseModel):
    title: str
    description: str


class CreateToBuyListCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    to_buy_list_repository: inventory_repositories.ToBuyListRepository[
        model_to_buy.FoodTrackToBuy,
        shared_to_buy_id.FoodTrackToBuyId,
    ]

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies):
        self.uow = dependencies.uow
        self.logger = dependencies.logger
        self.to_buy_list_repository = dependencies.repository_store.build(
            inventory_repositories.ToBuyListRepository[
                model_to_buy.FoodTrackToBuy,
                shared_to_buy_id.FoodTrackToBuyId,
            ]
        )

    def execute(self, create_to_buy_dto: CreateToBuyListDTO) -> model_to_buy.FoodTrackToBuy:
        to_buy_created = model_to_buy.FoodTrackToBuy.create(
            create_dto=model_to_buy.CreateFoodTrackToBuyDTO(
                title=create_to_buy_dto.title,
                description=create_to_buy_dto.description,
                is_bought=False,
            )
        )

        return self.to_buy_list_repository.create(entity=to_buy_created)


class CreateToBuyItemDTO(pydantic.BaseModel):
    name: str
    comment: str
    to_buy_list: shared_to_buy_id.FoodTrackToBuyId
    inventory_id: shared_inventory_id.InventoryID
    quantity: shared_quantity.Quantity


class CreateItemIntoToBuyListCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    to_buy_items_repository:  inventory_repositories.ToBuyItemListRepository[
        model_to_buy.FoodTrackToBuyItem,
        shared_to_buy_id.FoodTrackItemToBuyId,
    ]

    def __init__(self, dependencies: domain_dependencies.ExtendedControllerDependencies):
        self.uow = dependencies.uow
        self.logger = dependencies.logger
        self.to_buy_items_repository = dependencies.repository_store.build(
            inventory_repositories.ToBuyItemListRepository[
                model_to_buy.FoodTrackToBuyItem,
                shared_to_buy_id.FoodTrackItemToBuyId,
            ]
        )

    def execute(self, create_to_buy_item_dto: CreateToBuyItemDTO) -> model_to_buy.FoodTrackToBuyItem:
        to_buy_item_created = model_to_buy.FoodTrackToBuyItem.create(
            create_dto=model_to_buy.CreateFoodTrackToBuyItemDTO(
                name=create_to_buy_item_dto.name,
                comment=create_to_buy_item_dto.comment,
                quantity=create_to_buy_item_dto.quantity,
                to_buy_id=create_to_buy_item_dto.to_buy_list,
                inventory_id=create_to_buy_item_dto.inventory_id,
            )
        )

        return self.to_buy_items_repository.create(entity=to_buy_item_created)
