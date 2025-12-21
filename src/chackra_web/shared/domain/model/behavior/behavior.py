from typing import Protocol, TypeVar

M = TypeVar("M")
ID = TypeVar("ID")


class CreatorBehavior(Protocol[M]):
    def __init__(self, uow) -> None: ...

    def create(self, entity: M) -> M:
        raise NotImplementedError()


class UpdaterBehavior(Protocol[M, ID]):
    def __init__(self, uow) -> None: ...

    def update(self, id: ID, entity: M) -> M:
        raise NotImplementedError()


class DeleterBehavior(Protocol[ID]):
    def __init__(self, uow) -> None: ...

    def delete(self, id: ID) -> None:
        raise NotImplementedError()


class FinderBehavior(Protocol[M, ID]):
    def __init__(self, uow) -> None: ...

    def find_by_id(self, id: ID) -> M | None:
        raise NotImplementedError()
