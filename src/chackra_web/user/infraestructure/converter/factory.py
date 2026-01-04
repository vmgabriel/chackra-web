from chackra_web.shared.domain.model.converter_entity import converter as shared_converter
from chackra_web.user.infraestructure.converter.flask import list_user_html, filter_user

from chackra_web.shared.domain.model.configuration import configuration as shared_configuration


flask_converters: dict[str, shared_converter.AbstractConverter] = {
    "list_user": list_user_html.ListUserFlaskHtml(),
    "filter_user": filter_user.FilterUserFlaskHtml(),
}

converters: dict[str, dict[str, shared_converter.AbstractConverter]] = {
    "flask": flask_converters,
}


def get_converter(configuration: shared_configuration.Configuration) -> dict[str, shared_converter.AbstractConverter]:
    converter_attribute = "converter_adapter"

    return converters.get(getattr(configuration, converter_attribute, "flask"), {})
