import pydantic

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger

from chackra_web.food_track.domain.models import (
    exceptions as food_track_exceptions,
    to_buy as model_to_buy,
    repositories as inventory_repositories
)

from chackra_web.shared.domain.model.food_track import to_buy as shared_to_buy_id
from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies

from chackra_web.food_track.domain.services.to_buy import get_by_id as get_by_id_service


class GetByIdToBuyListIdDTO(pydantic.BaseModel):
    id: str


class GetByIdToBuyListCommand:
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
    to_buy_list_repository:  inventory_repositories.ToBuyListRepository[
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

    def execute(self, get_by_id: GetByIdToBuyListIdDTO) -> model_to_buy.FoodTrackToBuy:
        to_buy_list_id = shared_to_buy_id.FoodTrackToBuyId(value=get_by_id.id)
        to_buy_list = get_by_id_service.get_by_id(
            id=to_buy_list_id,
            to_buy_list_repository=self.to_buy_list_repository
        )
        if not to_buy_list:
            raise food_track_exceptions.ToBuyListNotFoundException()

        return to_buy_list
