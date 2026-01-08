import abc
import enum

import flask
import pydantic
import dataclasses

from chackra_web.shared.domain.model.specifications import specifications as shared_specifications


class OrderType(enum.StrEnum):
    ASC = "ASC"
    DESC = "DESC"


class Ordered(abc.ABC):
    type: OrderType = OrderType.ASC
    attribute: str

    def __init__(self, attribute: str) -> None:
        self.attribute = attribute

    @abc.abstractmethod
    def to_sql(self) -> str:
        raise NotImplementedError()


class AscOrdered(Ordered, abc.ABC):
    ...


class DescOrdered(Ordered, abc.ABC):
    type = OrderType.DESC


class Pagination(abc.ABC):
    filters: shared_specifications.BaseSpecification | None = None
    order_by: list[Ordered] | None = None
    page: int
    page_size: int

    def __init__(
            self,
            page: int,
            page_size: int,
            order_by: list[Ordered] | None = None,
            filters: shared_specifications.BaseSpecification | None = None
    ) -> None:
        self.filters = filters
        self.page = page
        self.page_size = page_size
        self.order_by = order_by

    @abc.abstractmethod
    def page_to_sql(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def page_size_to_sql(self) -> str:
        raise NotImplementedError()


@dataclasses.dataclass
class Paginator:
    page_size: int
    page: int
    total: int
    entities: list[object] = dataclasses.field(default_factory=list)

    @property
    def start(self) -> int:
        return self.page_size * (self.page - 1)

    @property
    def end(self) -> int:
        return self.start + self.page_size

    @property
    def total_pages(self) -> int:
        return (self.total // self.page_size) + 1

    @property
    def has_previous(self) -> bool:
        return self.page not in (0, 1)

    @property
    def has_next(self) -> bool:
        return self.total_pages < self.page

    @property
    def prev_page(self) -> int:
        return self.page - 1 if self.has_previous else self.page

    @property
    def __next__(self) -> int:
        return self.page + 1 if self.has_next else self.page

    @property
    def pages(self) -> list[int]:
        response = [self.page]
        current_pages = [self.page - 2, self.page - 1, self.page + 1, self.page + 2]
        for current_page in current_pages:
            if current_page <= 0:
                continue
            if current_page > self.total_pages:
                continue
            response.append(current_page)
        return response


class PaginatorExtended(Paginator):
    headers: dict[str, str] = dataclasses.field(default_factory=dict)
    update_url: str | None = None
    delete_url: str | None = None
    show_url: str | None = None
    title: str = ""
    message_delete: str = ""
    title_delete: str = ""
    current_endpoint: str = ""
    filter_convertion: str = ""
    list_convertion: str = ""
    url_current_keys: dict[str, str] = dataclasses.field(default_factory=dict)
    url_keys: dict[str, str] | None = None
    filters: list[str] = dataclasses.field(default_factory=list)

    @staticmethod
    def from_paginator(paginator: Paginator) -> 'PaginatorExtended':
        return PaginatorExtended(**dataclasses.asdict(paginator))
