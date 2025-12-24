from typing import Protocol, TypeVar

M = TypeVar("M")
ID = TypeVar("ID")


class CreatorBehavior(Protocol[M]):
    def create(self, entity: M) -> M:
        raise NotImplementedError()


class UpdaterBehavior(Protocol[M, ID]):
    def update(self, id: ID, entity: M) -> M:
        raise NotImplementedError()


class DeleterBehavior(Protocol[ID]):
    def delete(self, id: ID) -> None:
        raise NotImplementedError()


class FinderBehavior(Protocol[M, ID]):
    def find_by_id(self, id: ID) -> M | None:
        raise NotImplementedError()
