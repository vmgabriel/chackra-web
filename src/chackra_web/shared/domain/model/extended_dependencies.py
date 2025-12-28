import dataclasses

from chackra_web.shared.domain.model import dependencies as shared_dependencies
from chackra_web.shared.domain.model.repository import builder as shared_repository
from chackra_web.shared.domain.model.specifications import (
    builder as shared_specifications,
    conversion as shared_specifications_conversion
)
from chackra_web.shared.domain.model.pagination import (
    builder as shared_pagination,
    conversion as shared_pagination_conversion
)


@dataclasses.dataclass
class ExtendedControllerDependencies(shared_dependencies.ControllerDependencies):
    repository_store: shared_repository.RepositoryStore
    specification_builder: shared_specifications.SpecificationBuilder
    paginator_builder: shared_pagination.PaginationBuilder
    to_specification_builder: shared_specifications_conversion.ToSpecifications
    to_pagination_builder: shared_pagination_conversion.ToConversion

    @staticmethod
    def from_dependencies(
        controller_dependencies: shared_dependencies.ControllerDependencies,
        repository_store: shared_repository.RepositoryStore,
        specification_builder: shared_specifications.SpecificationBuilder,
        paginator_builder: shared_pagination.PaginationBuilder,
        to_specification_builder: shared_specifications_conversion.ToSpecifications,
        to_pagination_builder: shared_pagination_conversion.ToConversion,
    ) -> "ExtendedControllerDependencies":
        return ExtendedControllerDependencies(
            configuration=controller_dependencies.configuration,
            logger=controller_dependencies.logger,
            uow=controller_dependencies.uow,
            repository_store=repository_store,
            specification_builder=specification_builder,
            paginator_builder=paginator_builder,
            to_specification_builder=to_specification_builder,
            to_pagination_builder=to_pagination_builder,
        )