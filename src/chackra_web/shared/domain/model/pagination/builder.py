from typing import Type

from chackra_web.shared.domain.model.pagination import pagination as shared_pagination


class PaginationBuilder:
    asc_ordered: Type[shared_pagination.AscOrdered]
    desc_ordered: Type[shared_pagination.DescOrdered]
    pagination: Type[shared_pagination.Pagination]

    def __init__(
        self,
        asc_ordered: Type[shared_pagination.AscOrdered],
        desc_ordered: Type[shared_pagination.DescOrdered],
        pagination: Type[shared_pagination.Pagination]
    ) -> None:
        self.asc_ordered = asc_ordered
        self.desc_ordered = desc_ordered
        self.pagination = pagination

    def get_pagination(self) -> Type[shared_pagination.Pagination]:
        return self.pagination

    def get_ordered(self, type_order: shared_pagination.OrderType) -> Type[shared_pagination.Ordered]:
        if type_order == shared_pagination.OrderType.ASC:
            return self.asc_ordered
        return self.desc_ordered