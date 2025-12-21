from typing import Generic

from chackra_web.shared.domain.model import dependencies as shared_dependencies
from chackra_web.shared.domain.model.behavior import behavior as shared_behavior


class GenericRepository(Generic[shared_behavior.M, shared_behavior.ID]):
    def __init__(
            self,
            dependencies: shared_dependencies.ControllerDependencies,
            creator: shared_behavior.CreatorBehavior[shared_behavior.M],
            finder: shared_behavior.FinderBehavior[shared_behavior.M, shared_behavior.ID]
    ) -> None:
        self.creator = creator
        self.finder = finder
        self.dependencies = dependencies

    def create(self, entity: shared_behavior.M) -> shared_behavior.M:
        return self.creator.create(entity)

    def find_by_id(self, id: shared_behavior.ID) -> shared_behavior.M | None:
        return self.finder.find_by_id(id)

