import abc
import enum
import pydantic

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


class Paginator(pydantic.BaseModel):
    page_size: int
    page: int
    total: int
    entities: list[object] = pydantic.Field(default_factory=list)

    @property
    def total_pages(self) -> int:
        return self.total // self.page_size

    @property
    def has_previous(self) -> bool:
        return self.page not in (0, 1)

    @property
    def has_next(self) -> bool:
        return self.total_pages < self.page