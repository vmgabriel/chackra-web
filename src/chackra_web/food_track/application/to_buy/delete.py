import pydantic

from chackra_web.shared.domain.model import extended_dependencies as domain_dependencies
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.food_track import to_buy as shared_to_buy_id

from chackra_web.food_track.domain.models import (
    to_buy as model_to_buy,
    exceptions as food_tracking_exceptions,
    repositories as inventory_repositories
)

from chackra_web.food_track.domain.services.to_buy import delete as to_buy_delete


class DeleteToBuyListDTO(pydantic.BaseModel):
    id: str


class DeleteToBuyListCommand:
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

    def execute(self, delete_request: DeleteToBuyListDTO) -> None:
        try:
            to_buy_delete.delete_to_buy_list(
                id=shared_to_buy_id.FoodTrackToBuyId(value=delete_request.id),
                to_buy_list_repository=self.to_buy_list_repository
            )
        except food_tracking_exceptions.ToBuyListHasAlreadyDeletedException:
            self.logger.info("To Buy List '{}' has already been deleted".format(delete_request.id))
            return None
