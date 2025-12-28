import abc

from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.pagination import (
    builder as shared_pagination_builder,
    pagination as shared_pagination
)


class ToConversion(abc.ABC):
    logger: shared_logger.LogAdapter
    pagination_builder: shared_pagination_builder.PaginationBuilder

    def __init__(
            self,
            logger: shared_logger.LogAdapter,
            pagination_builder: shared_pagination_builder.PaginationBuilder,
    ) -> None:
        self.logger = logger
        self.pagination_builder = pagination_builder

    @abc.abstractmethod
    def to_ordered(self, key: str) -> shared_pagination.Ordered:
        raise NotImplementedError()

