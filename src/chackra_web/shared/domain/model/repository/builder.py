from typing import TypeVar, Type

import dataclasses
import inspect

from chackra_web.shared.domain.model import dependencies as shared_dependencies
from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.shared.domain.model.repository import repository as shared_repository


M = TypeVar("M", bound=shared_repository.GenericRepository)
ME = TypeVar("ME")
F = TypeVar("F", bound=shared_behavior.FinderBehavior[shared_behavior.M, shared_behavior.ID])


@dataclasses.dataclass
class PreDefinitionRepository:
    repository: Type[M]
    creator: Type[shared_behavior.CreatorBehavior[shared_behavior.M]]
    finder: Type[F]
    listener: Type[shared_behavior.ListerBehavior[shared_behavior.M]] | None = None
    updater: Type[shared_behavior.UpdaterBehavior[shared_behavior.M, shared_behavior.ID]] | None = None
    deleter: Type[shared_behavior.DeleterBehavior[shared_behavior.ID]] | None = None

    def build(self, dependencies: shared_dependencies.ControllerDependencies) -> M:
        params = {
            "dependencies": dependencies,
            "finder": self.finder(dependencies.uow),
            "creator": self.creator(dependencies.uow),
        }
        if self.listener:
            params["listener"] = self.listener(dependencies.uow)
        if self.updater:
            params["updater"] = self.updater(dependencies.uow)
        if self.deleter:
            params["deleter"] = self.deleter(dependencies.uow)

        return self.repository(**params)


class RepositoryStore:
    dependencies: shared_dependencies.ControllerDependencies
    store: dict[Type[M], PreDefinitionRepository]

    def __init__(self, dependencies: shared_dependencies.ControllerDependencies) -> None:
        self.dependencies = dependencies
        self.store = {}

    def add(
            self,
            pre_definition: PreDefinitionRepository,
    ) -> None:
        if pre_definition.repository in self.store:
            return
        self.store[pre_definition.repository] = pre_definition

    def build(self, repository_type: Type[M]) -> M:
        return self.store[repository_type].build(dependencies=self.dependencies)

    def __add__(self, other: "RepositoryStore") -> "RepositoryStore":
        new_repository_store = RepositoryStore(dependencies=self.dependencies)
        for repository in self.store.values():
            new_repository_store.add(repository)
        for repository in other.store.values():
            new_repository_store.add(repository)
        return new_repository_store
