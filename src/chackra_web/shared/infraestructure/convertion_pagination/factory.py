from typing import Type

from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.pagination import (
    conversion as shared_pagination_conversion,
    builder as shared_pagination_builder,
)

from chackra_web.shared.infraestructure.convertion_pagination.flask import convertion as shared_flask_convertion

to_convertion_handler: dict[str, Type[shared_pagination_conversion.ToConversion]] = {
    "flask": shared_flask_convertion.FlaskRequestToPagination,
}


class ToConvertionFactory:
    name_configuration_attribute: str = "to_convertion_adapter"

    def build(
            self,
            configuration: shared_configuration.Configuration,
            logger: shared_logger.LogAdapter,
            pagination_builder: shared_pagination_builder.PaginationBuilder
    ) -> shared_pagination_conversion.ToConversion:
        pagination_factory_value = getattr(configuration, self.name_configuration_attribute, "flask").lower()
        handlers = to_convertion_handler.get(pagination_factory_value)
        return handlers(logger=logger, pagination_builder=pagination_builder)