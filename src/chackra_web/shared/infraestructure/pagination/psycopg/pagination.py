from chackra_web.shared.domain.model.pagination import pagination as shared_pagination


class PsycopgPagination(shared_pagination.Pagination):
    def page_to_sql(self) -> str:
        return f"OFFSET {(self.page - 1) * self.page_size}"

    def page_size_to_sql(self) -> str:
        return f"LIMIT {self.page_size}"


class PsycopgAscOrdered(shared_pagination.AscOrdered):
    type: shared_pagination.OrderType = shared_pagination.OrderType.ASC

    def to_sql(self) -> str:
        return f"{self.attribute} ASC"


class PsycopgDescOrdered(shared_pagination.DescOrdered):
    def to_sql(self) -> str:
        return f"{self.attribute} DESC"