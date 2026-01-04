from typing import Callable

from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.converter_entity import  converter as converter_entity, factory as converter_factory

from chackra_web.shared.infraestructure.handlers.flask import list_handler, pagination


handlers: dict[str, list[Callable]] = {
    "flask": [
        list_handler.to_html,
        pagination.dynamic_url,
    ]
}


def inject_converters(name: str, converter: converter_entity.AbstractConverter) -> None:
    converter_factory.CURRENT_CONVERTER_FACTORY.inject(name=name, converter=converter)


def get_handlers(configuration: shared_configuration.Configuration) -> list[Callable]:
    name_configuration_attribute: str = "handler_adapter"
    return handlers.get(getattr(configuration, name_configuration_attribute, "flask"), [])