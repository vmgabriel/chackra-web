from typing import Any
import markupsafe

from chackra_web.shared.domain.model.converter_entity import converter as shared_converter


class ListUserFlaskHtml(shared_converter.AbstractConverter):
    def _default_show(value: Any) -> object:
        if value is None:
            return ""
        return markupsafe.Markup(markupsafe.escape(str(value)))

    @staticmethod
    def show_initials(value: Any) -> str:
        initial_html = """
        <div class="avatar me-3">
            <div 
                class="rounded-circle bg-primary bg-opacity-10 text-primary d-flex align-items-center justify-content-center" 
                style="width: 40px; height: 40px;"
            >
                {value}
            </div>
        </div>
        """
        if value is None:
            return ""

        return markupsafe.Markup(initial_html.format(
            value=markupsafe.escape(value.upper())
        ))

    @staticmethod
    def show_auth_role  (value: str) -> str:
        initial_html = """
        <span class="badge rounded-pill {color_role}">
            {value}
        </span>
        """
        if value is None:
            return ""

        match value.lower():
            case "admin":
                color_role = "bg-danger"
            case "editor":
                color_role = "bg-warning"
            case _:
                color_role = "bg-info"

        return markupsafe.Markup(initial_html.format(
            value=markupsafe.escape(value.upper()),
            color_role=color_role,
        ))

    @staticmethod
    def show_active(value: str) -> str:
        initial_html = """
        <div class="form-check form-switch">
            <input
                class="form-check-input"
                type="checkbox" 
                {is_checked} 
                disabled
            >
        </div>
        """
        if value is None:
            return ""

        is_checked = ""
        if value == "true" or value == True:
            is_checked = "checked"

        return markupsafe.Markup(
            initial_html.format(is_checked=is_checked)
        )
