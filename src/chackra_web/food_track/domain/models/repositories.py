from chackra_web.shared.domain.model import dependencies as shared_dependencies
from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.shared.domain.model.repository import repository as shared_repository
from chackra_web.food_track.domain.models import behavior as food_track_behavior


class FoodTrackRepository:
    ...


class InventoryRepository(
    shared_repository.GenericRepository[shared_behavior.M, shared_behavior.ID]
):
    def __init__(
            self,
            dependencies: shared_dependencies.ControllerDependencies,
            creator: shared_behavior.CreatorBehavior[shared_behavior.M],
            finder: food_track_behavior.InventoryFinderBehavior[shared_behavior.M, shared_behavior.ID],
    ) -> None:
        super().__init__(dependencies, creator, finder)
        self._name_finder = finder

    def find_by_name(self, name: str) -> shared_behavior.M | None:
        return self._name_finder.find_by_name(name)
