from chackra_web.shared.domain.model.food_track import to_buy as shared_to_buy_id
from chackra_web.food_track.domain.models import (
    to_buy as model_to_buy,
    repositories as food_track_repositories,
    exceptions as food_track_exceptions,
)
from chackra_web.food_track.domain.services.to_buy import get_by_id as to_buy_get_by_id_service

def update_to_buy_list(
        id: shared_to_buy_id.FoodTrackToBuyId,
        changes: model_to_buy.UpdateFoodTrackToBuyDTO,
        to_buy_list_repository: food_track_repositories.ToBuyListRepository[
            model_to_buy.FoodTrackToBuy,
            shared_to_buy_id.FoodTrackToBuyId,
        ]
) -> model_to_buy.FoodTrackToBuy:
    to_buy_list = to_buy_get_by_id_service.get_by_id(id=id, to_buy_list_repository=to_buy_list_repository)
    if not to_buy_list:
        raise food_track_exceptions.ToBuyListNotFoundException()

    return to_buy_list_repository.update(id=id, entity=to_buy_list.update(changes))


def update_to_buy_item(
        id: shared_to_buy_id.FoodTrackItemToBuyId,
        changes: model_to_buy.UpdateFoodTrackToBuyItemDTO,
        to_buy_items_repository: food_track_repositories.ToBuyItemListRepository[
            model_to_buy.FoodTrackToBuyItem,
            shared_to_buy_id.FoodTrackItemToBuyId,
        ]
) -> model_to_buy.FoodTrackToBuyItem:
    to_buy_item = to_buy_get_by_id_service.get_item_by_id(id=id, to_buy_items_repository=to_buy_items_repository)
    if not to_buy_item:
        raise food_track_exceptions.ToBuyItemNotExistsException()

    return to_buy_items_repository.update(id=id, entity=to_buy_item.update(changes=changes))
