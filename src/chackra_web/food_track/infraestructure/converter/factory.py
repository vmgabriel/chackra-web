from chackra_web.shared.domain.model.converter_entity import converter as shared_converter
from chackra_web.food_track.infraestructure.converter.flask import list_inventory_html, filter_inventory
from chackra_web.food_track.infraestructure.converter.flask.to_buy import list as list_to_buy_html, filter as filter_to_buy_html

from chackra_web.shared.domain.model.configuration import configuration as shared_configuration


flask_converters: dict[str, shared_converter.AbstractConverter] = {
    "list_inventory": list_inventory_html.ListInventoryFlaskHtml(),
    "filter_inventory": filter_inventory.FilterInventoryFlaskHtml(),
    "list_to_buy_lists": list_to_buy_html.ListToBuyListFlaskHtml(),
    "filter_to_buy_lists": filter_to_buy_html.FilterToBuyListFlaskHtml(),
}

converters: dict[str, dict[str, shared_converter.AbstractConverter]] = {
    "flask": flask_converters,
}


def get_converter(configuration: shared_configuration.Configuration) -> dict[str, shared_converter.AbstractConverter]:
    converter_attribute = "converter_adapter"

    return converters.get(getattr(configuration, converter_attribute, "flask"), {})
