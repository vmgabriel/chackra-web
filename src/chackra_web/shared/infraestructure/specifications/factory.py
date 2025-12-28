from typing import Type

from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.logger import logger as shared_logger

from chackra_web.shared.domain.model.specifications import (
    specifications as shared_specifications,
    builder as shared_builder
)
from chackra_web.shared.infraestructure.specifications.psycopg import converter as shared_psycopg_converters


specifications_handlers: dict[
    str,
    tuple[shared_specifications.ConvertersSpecification, Type[shared_specifications.BaseSpecification]]
] = {
    "psycopg": (
        shared_psycopg_converters.PsycopgConvertersSpecification(),
        shared_psycopg_converters.PsycopgBaseSpecification
    ),
}


class SpecificationsGenericsFactory:
    name_configuration_attribute: str = "specification_adapter"

    def build(
            self,
            configuration: shared_configuration.Configuration,
            logger: shared_logger.LogAdapter,
    ) -> shared_builder.SpecificationBuilder:
        specification_factory_value = getattr(configuration, self.name_configuration_attribute, "psycopg").lower()
        handlers, base_handler = specifications_handlers.get(specification_factory_value)
        return shared_builder.SpecificationBuilder(handlers, base_handler)
