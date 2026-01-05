from chackra_web.shared.domain.model.food_track import to_buy as shared_to_buy_id
from chackra_web.food_track.domain.models import (
    to_buy as model_to_buy,
    repositories as food_track_repositories,
    exceptions as food_track_exceptions
)

from chackra_web.food_track.domain.services.to_buy import get_by_id as to_buy_get_by_id


def delete_to_buy_list(
    id: shared_to_buy_id.FoodTrackToBuyId,
    to_buy_list_repository: food_track_repositories.ToBuyListRepository[
        model_to_buy.FoodTrackToBuy,
        shared_to_buy_id.FoodTrackToBuyId
    ]
) -> None:
    to_buy_item = to_buy_get_by_id.get_by_id(id=id, to_buy_list_repository=to_buy_list_repository)
    if not to_buy_item:
        raise food_track_exceptions.ToBuyListNotFoundException()

    to_buy_item.delete()

    to_buy_list_repository.update(id=id, entity=to_buy_item)
