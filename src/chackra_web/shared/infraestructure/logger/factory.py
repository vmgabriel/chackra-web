from typing import Type, TypeVar

from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.infraestructure.logger import logging as shared_logging

T = TypeVar("T", bound=shared_logger.LogAdapter)


logger_factories: dict[str, Type[T]] = {
    "logging":  shared_logging.LoggingAdapter,
}


class LoggerFactory:
    name_configuration_attribute: str = "logger_adapter"

    def build(self, configuration: shared_configuration.Configuration) -> T:
        logging_factory_value = getattr(configuration, self.name_configuration_attribute, "logging").lower()
        adapter = logger_factories.get(logging_factory_value)

        return adapter(configuration=configuration)
