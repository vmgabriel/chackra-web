from typing import Any
import markupsafe

from chackra_web.shared.domain.model.converter_entity import converter as shared_converter


class FilterInventoryFlaskHtml(shared_converter.AbstractConverter):
    def _default_show(value: Any) -> object:
        if value is None:
            return ""
        return markupsafe.Markup(markupsafe.escape(str(value)))

    @staticmethod
    def show_search(value: Any) -> str:
        current_value = 'value="{value}"'.format(value=value)
        return markupsafe.Markup(
            """
            <input type="text"
                class="form-control"
                name="search"
                placeholder="search..."
                {current_value}
            >
            """.format(current_value=current_value if value else "")
        )

    @staticmethod
    def show_state(value: bool) -> str:
        selected_true = ""
        selected_false = ""
        selected_none = ""
        if value is None:
            selected_none = "selected"
        elif value:
            selected_true = "selected"
        else:
            selected_false = "selected"

        return markupsafe.Markup(
            """
            <select class="form-select" name="state">
                <option value="" {selected_none}>No se ha seleccionado</option>
                <option value="true" {selected_true}>
                    Disponible
                </option>
                <option value="false" {selected_false}>
                    No Disponible
                </option>
            </select>
            """.format(selected_true=selected_true, selected_false=selected_false, selected_none=selected_none)
        )
