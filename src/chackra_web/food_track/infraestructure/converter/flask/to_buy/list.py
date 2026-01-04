from typing import Any
import markupsafe

from chackra_web.shared.domain.model.converter_entity import converter as shared_converter


class ListToBuyListFlaskHtml(shared_converter.AbstractConverter):
    def _default_show(value: Any) -> object:
        if value is None:
            return ""
        return markupsafe.Markup(markupsafe.escape(str(value)))

    @staticmethod
    def show_is_bought(value: bool) -> str:
        if value is None:
            return ""
        if value:
            return markupsafe.Markup('<span class="badge bg-danger">No Comprado Aun</span>')
        return markupsafe.Markup('<span class="badge bg-success">Ya Comprado</span>')
