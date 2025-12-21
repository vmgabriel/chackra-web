import dataclasses

from chackra_web.shared.domain.model import dependencies as shared_dependencies
from chackra_web.shared.domain.model.repository import builder as shared_repository


@dataclasses.dataclass
class ExtendedControllerDependencies(shared_dependencies.ControllerDependencies):
    repository_store: shared_repository.RepositoryStore

    @staticmethod
    def from_dependencies(
            controller_dependencies: shared_dependencies.ControllerDependencies,
            repository_store: shared_repository.RepositoryStore
    ) -> "ExtendedControllerDependencies":
        return ExtendedControllerDependencies(
            configuration=controller_dependencies.configuration,
            logger=controller_dependencies.logger,
            uow=controller_dependencies.uow,
            repository_store=repository_store,
        )