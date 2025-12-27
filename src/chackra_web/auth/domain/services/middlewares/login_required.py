
from typing import Optional, Any, Callable
import functools

from chackra_web.web.domain.web import app as web_app


def find_attribute_or_redirect(context: web_app.Adapter) -> Any | None:
    user = context.get_auth_user()
    if not user:
        return context.redirect_to_login()


def find_role_or_redirect(context: web_app.Adapter, roles: Optional[list[str]] = None):
    roles = roles or []
    user = context.get_auth_user()
    if roles and user.role not in roles:
        return context.redirect_to_login()
    return None


def login_required(
        roles: Optional[list[str]] = None
) -> Callable:
    def middleware(context: web_app.Adapter, handler: Callable) -> Callable:
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            redirect_response = find_attribute_or_redirect(context)
            if redirect_response:
                return redirect_response

            redirect_response = find_role_or_redirect(context, roles)
            if redirect_response:
                return redirect_response

            return handler(*args, **kwargs)
        return wrapper
    return middleware

