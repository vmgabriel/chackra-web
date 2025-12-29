from typing import Protocol, TypeVar

from chackra_web.shared.domain.model.pagination import pagination as shared_pagination

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


class ListerBehavior(Protocol[M]):
    def matching(self, pagination: shared_pagination.Pagination) -> shared_pagination.Paginator:
        raise NotImplementedError()