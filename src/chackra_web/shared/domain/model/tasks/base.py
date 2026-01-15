from __future__ import annotations
from typing import Any, Type
import abc

from chackra_web.shared.domain.model import extended_dependencies as shared_dependencies


class Task(abc.ABC):
    name: str

    @abc.abstractmethod
    def execute(
            self,
            dependencies: shared_dependencies.ExtendedControllerDependencies | None = None,
            **kwargs
    ) -> Any:
        raise NotImplementedError()


class TaskRegistry:
    def __init__(self, namespace: str):
        self.namespace = namespace
        self._tasks: dict[str, Task] = {}

    def register(self, task_class: Type[Task]) -> None:
        task = task_class()
        self._tasks[task.name] = task

    def execute(
            self,
            task_name: str,
            dependencies: shared_dependencies.ExtendedControllerDependencies | None = None,
            **kwargs
    ) -> Any:
        if task_name not in self._tasks:
            raise ValueError(f"Task {task_name} not found")
        return self._tasks[task_name].execute(dependencies=dependencies, **kwargs)


class TaskQueueAdapter(abc.ABC):
    @abc.abstractmethod
    def enqueue(self, full_task_name: str, kwargs: dict[str, Any]) -> None:
        raise NotImplementedError()


class TaskQueueAdapterApp(TaskQueueAdapter, abc.ABC):
    app: object
    registries: dict[str, TaskRegistry]

    dependencies: shared_dependencies.ExtendedControllerDependencies

    def __init__(self, dependencies: shared_dependencies.ExtendedControllerDependencies) -> None:
        self.dependencies = dependencies

    @abc.abstractmethod
    def _setup(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_app_instance(self) -> object:
        raise NotImplementedError()

    def register(self, registry: TaskRegistry) -> None:
        if registry.namespace in self.registries:
            raise ValueError(f"Registry {registry.namespace} already registered")
        self.registries[registry.namespace] = registry
