import pydantic

from chackra_web.food_track.domain.models import (
    to_buy as model_to_buy,
    repositories as inventory_repositories
)

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.food_track import to_buy as shared_to_buy_id


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
