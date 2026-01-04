from typing import Any
import markupsafe

from chackra_web.shared.domain.model.converter_entity import converter as shared_converter


class FilterUserFlaskHtml(shared_converter.AbstractConverter):
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
    def show_role(value: str) -> str:
        selected_none = ""
        selected_admin = ""
        selected_user = ""
        if value is None:
            selected_none = "selected"
        elif value.lower() == "admin":
            selected_admin = "selected"
        else:
            selected_user = "selected"

        return markupsafe.Markup(
            """
            <select class="form-select" name="role">
                <option value="" {selected_none}>Todos los Roles</option>
                <option value="true" {selected_admin}>
                    Administrador
                </option>
                <option value="false" {selected_user}>
                    Usuario
                </option>
            </select>
            """.format(
                selected_admin=selected_admin,
                selected_user=selected_user,
                selected_none=selected_none
            )
        )

    @staticmethod
    def show_active(value: str) -> str:
        selected_none = ""
        selected_active = ""
        selected_inactive = ""
        if value is None:
            selected_none = "selected"
        elif value == "true":
            selected_active = "selected"
        else:
            selected_inactive = "selected"

        return markupsafe.Markup(
            """
            <select class="form-select" name="active">
                <option value="" {selected_none}>Todos los estados</option>
                <option value="true" {selected_active}>
                    Activo
                </option>
                <option value="false" {selected_inactive}>
                    Inactivo
                </option>
            </select>
            """.format(
                selected_none=selected_none,
                selected_active=selected_active,
                selected_inactive=selected_inactive
            )
        )

    @staticmethod
    def show_id(value: str) -> str:
        return markupsafe.Markup("")