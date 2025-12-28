from typing import Any
import abc

from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.specifications import (
    specifications as shared_specifications,
    builder as shared_specification_builder
)


class ToSpecifications(abc.ABC):
    logger: shared_logger.LogAdapter
    specification_builder: shared_specification_builder.SpecificationBuilder

    def __init__(
        self,
        specification_builder: shared_specification_builder.SpecificationBuilder,
        logger: shared_logger.LogAdapter,
    ) -> None:
        self.logger = logger
        self.specification_builder = specification_builder

    @abc.abstractmethod
    def to_specification(self, key: Any, value: Any) -> shared_specifications.BaseSpecification:
        raise NotImplementedError()
