from chackra_web.shared.domain.model import dependencies as shared_dependencies
from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.shared.domain.model.repository import repository as shared_repository


class FoodTrackRepository:
    ...


class InventoryRepository(
    shared_repository.GenericRepository[shared_behavior.M, shared_behavior.ID]
):
    def __init__(
            self,
            dependencies: shared_dependencies.ControllerDependencies,
            creator: shared_behavior.CreatorBehavior[shared_behavior.M],
            finder: shared_behavior.FinderBehavior[shared_behavior.M, shared_behavior.ID],
    ) -> None:
        super().__init__(dependencies, creator, finder)
