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
from chackra_web.shared.domain.model.tasks import base as shared_task_base
from chackra_web.shared.domain.model.llm import base as shared_llm_base


@dataclasses.dataclass
class ExtendedControllerDependencies(shared_dependencies.ControllerDependencies):
    repository_store: shared_repository.RepositoryStore
    specification_builder: shared_specifications.SpecificationBuilder
    paginator_builder: shared_pagination.PaginationBuilder
    to_specification_builder: shared_specifications_conversion.ToSpecifications
    to_pagination_builder: shared_pagination_conversion.ToConversion
    llm_adapter: shared_llm_base.GenericLLMPort

    _task_queue_adapter: shared_task_base.TaskQueueAdapterApp | None = None

    @staticmethod
    def from_dependencies(
        controller_dependencies: shared_dependencies.ControllerDependencies,
        repository_store: shared_repository.RepositoryStore,
        specification_builder: shared_specifications.SpecificationBuilder,
        paginator_builder: shared_pagination.PaginationBuilder,
        to_specification_builder: shared_specifications_conversion.ToSpecifications,
        to_pagination_builder: shared_pagination_conversion.ToConversion,
        llm_adapter: shared_llm_base.GenericLLMPort
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
            llm_adapter=llm_adapter,
        )

    def inject_task_queue_adapter(self, task_queue_adapter: shared_task_base.TaskQueueAdapterApp) -> None:
        self._task_queue_adapter = task_queue_adapter

    def get_task_queue_instance(self) -> object:
        if self._task_queue_adapter is None:
            raise ValueError("Task queue adapter not injected")
        return self._task_queue_adapter.get_app_instance()

    def inject_periodic_builder_into_task_queue(self, periodic_task_base: shared_task_base.PeriodicTaskProxyBuilder) -> None:
        self._task_queue_adapter.add_periodic_task_builder(periodic_task_base)
