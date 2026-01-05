from chackra_web.shared.domain.model.food_track import to_buy as shared_to_buy_id
from chackra_web.food_track.domain.models import to_buy as model_to_buy, repositories as food_track_repositories


def get_by_id(
    id: shared_to_buy_id.FoodTrackToBuyId,
    to_buy_list_repository: food_track_repositories.ToBuyListRepository[
        model_to_buy.FoodTrackToBuy,
        shared_to_buy_id.FoodTrackToBuyId
    ]
) -> model_to_buy.FoodTrackToBuy | None:
    return to_buy_list_repository.find_by_id(id)