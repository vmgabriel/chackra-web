import pydantic

from chackra_web.food_track.domain.models import (
    to_buy as model_to_buy,
    repositories as food_track_repositories
)

from chackra_web.shared.domain.model.food_track import to_buy as shared_to_buy_id
from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger

from chackra_web.food_track.domain.services.to_buy import update as update_to_buy


class UpdateToBuyListRequestDTO(pydantic.BaseModel):
    id: str
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
