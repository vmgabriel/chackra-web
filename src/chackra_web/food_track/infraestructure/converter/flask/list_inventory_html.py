from typing import Any
import markupsafe

from chackra_web.shared.domain.model.converter_entity import converter as shared_converter


class ListInventoryFlaskHtml(shared_converter.AbstractConverter):
    def _default_show(value: Any) -> object:
        if value is None:
            return ""
        return markupsafe.Markup(markupsafe.escape(str(value)))

    @staticmethod
    def show_quantity(value: Any) -> str:
        if value is None:
            return ""
        return markupsafe.Markup(
            markupsafe.escape(str(value))
        )

    @staticmethod
    def show_is_sold_out(value: bool) -> str:
        if value is None:
            return ""
        if value:
            return markupsafe.Markup('<span class="badge bg-danger">No Available</span>')
        return markupsafe.Markup('<span class="badge bg-success">Available</span>')
