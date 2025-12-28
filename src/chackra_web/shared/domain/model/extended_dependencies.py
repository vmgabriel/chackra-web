import dataclasses

from chackra_web.shared.domain.model import dependencies as shared_dependencies
from chackra_web.shared.domain.model.repository import builder as shared_repository
from chackra_web.shared.domain.model.specifications import builder as shared_specifications
from chackra_web.shared.domain.model.pagination import builder as shared_pagination


@dataclasses.dataclass
class ExtendedControllerDependencies(shared_dependencies.ControllerDependencies):
    repository_store: shared_repository.RepositoryStore
    specification_store: shared_specifications.SpecificationStore
    paginator_builder: shared_pagination.PaginationBuilder

    @staticmethod
    def from_dependencies(
        controller_dependencies: shared_dependencies.ControllerDependencies,
        repository_store: shared_repository.RepositoryStore,
        specification_store: shared_specifications.SpecificationStore,
        paginator_builder: shared_pagination.PaginationBuilder,
    ) -> "ExtendedControllerDependencies":
        return ExtendedControllerDependencies(
            configuration=controller_dependencies.configuration,
            logger=controller_dependencies.logger,
            uow=controller_dependencies.uow,
            repository_store=repository_store,
            specification_store=specification_store,
            paginator_builder=paginator_builder
        )