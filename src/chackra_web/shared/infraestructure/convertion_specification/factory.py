from typing import Type
from chackra_web.shared.domain.model.specifications import (
    conversion as shared_specification_conversion,
    builder as shared_specification_builder
)
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.logger import logger as shared_logger

from chackra_web.shared.infraestructure.convertion_specification.flask import convertion as flask_convertion


to_specification_handler: dict[str, Type[shared_specification_conversion.ToSpecifications]] = {
    "flask": flask_convertion.FlaskRequestToSpecification,
}


class ToSpecificationFactory:
    name_configuration_attribute: str = "to_specification_adapter"

    def build(
        self,
        configuration: shared_configuration.Configuration,
        specification_builder: shared_specification_builder.SpecificationBuilder,
        logger: shared_logger.LogAdapter,
    ) -> shared_specification_conversion.ToSpecifications:
        to_specification_factory_value = getattr(configuration, self.name_configuration_attribute, "flask").lower()
        to_specification_adapter = to_specification_handler.get(to_specification_factory_value)

        return to_specification_adapter(specification_builder, logger)
