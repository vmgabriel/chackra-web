from typing import Callable, Any

import os
import flask
import functools

from chackra_web.shared.domain.model.web import route as shared_route
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.web.domain.web import app as web_app

from chackra_web.auth.domain.models import auth as auth_models, repositories as auth_repositories
from chackra_web.shared.domain.model.auth import auth_id as shared_auth_id
from chackra_web.auth.domain.services import get_session_by_auth_id as auth_get_session_by_auth_id


class FlaskAdapter(web_app.Adapter):
    configuration: dict[str, str] = {}

    def __init__(
            self,
            auth_repository: auth_repositories.AuthBaseRepository[auth_models.AuthUser, shared_auth_id.AuthId]
    ) -> None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        template_dir = os.path.join(base_dir, "presentation", "templates")
        static_dir = os.path.join(base_dir, "presentation", "static")


        _flask_app = flask.Flask(
            __name__,
            static_url_path="",
            static_folder=static_dir,
            template_folder=template_dir,
        )

        super().__init__(_flask_app, auth_repository)

    def _wrap_handler(self, route: shared_route.RouteDefinition) -> Callable:
        @functools.wraps(route.handler)
        def wrapped(*args, **kwargs):
            handler_params = route.handler.__code__.co_varnames[:route.handler.__code__.co_argcount]

            if "request" in handler_params:
                request_handler = FlaskRequestDataFactory()
                kwargs["request"] = request_handler.create(flask.request)

            if "user" in handler_params:
                kwargs["user"] = self.get_auth_user()

            result = route.handler(*args, **kwargs)

            if isinstance(result, flask.Response):
                return result

            if isinstance(result, shared_route.RouteResponse):
                if result.session and result.session.status is shared_route.StatusSession.SUCCESS:
                    flask.session["auth_id"] = result.session.auth_id
                    flask.g.auth_user = result.session
                if result.session and result.session.status is shared_route.StatusSession.LOGOUT:
                    flask.session.pop("auth_id", None)
                    flask.g.auth_user = None

                flask.flash(result.flash_message)
                return flask.redirect(flask.url_for(result.redirection))

            if route.template:
                if isinstance(result, dict):
                    return flask.render_template(route.template, **result)
                return flask.render_template(route.template, data=result)
            return result

        return wrapped

    def configure(self, configuration: shared_configuration.Configuration) -> None:
        self.configuration.update(configuration.dict())
        self.app.secret_key = self.configuration.get("SECRET_KEY", "secret")

    def register_route(self, route: shared_route.RouteDefinition) -> None:
        wrapped_handler = self._wrap_handler(route)

        if route.middleware:
            for middleware in route.middleware:
                wrapped_handler = middleware(self, wrapped_handler)

        self.app.add_url_rule(
            route.path,
            view_func=wrapped_handler,
            methods=[method.value for method in route.methods],
            endpoint=route.name
        )

    def get_auth_user(self) -> shared_route.Session | None:
        auth_user = flask.session.get("auth_user", None)
        if auth_user:
            return auth_user

        auth_id = flask.session.get("auth_id", None)
        if not auth_id:
            return None
        return self.get_session(auth_id)

    def get_session(self, auth_id: str) -> shared_route.Session | None:
        return auth_get_session_by_auth_id.get_session_by_auth_id(auth_id=auth_id, auth_repository=self.auth_repository)

    def redirect_to_login(self) -> Any:
        flask.flash("You must be logged in to access this page or you dont have permission to access this page.")
        return flask.redirect(flask.url_for("auth.login_get"))


    def build(self) -> object:
        return self.app


class FlaskWebApplicationFactory(web_app.WebAppFactory):
    def __init__(
            self,
            adapter: web_app.Adapter,
            configuration: shared_configuration.Configuration
    ) -> None:
        super().__init__(adapter, configuration)


class FlaskRequestDataFactory(shared_route.RequestDataFactory):
    def create(self, request: flask.Request) -> shared_route.RequestData:
        body = None
        if request.is_json:
            body = request.get_json()
        elif request.form:
            body = dict(request.form)

        return shared_route.RequestData(
            headers=dict(request.headers) if request.headers else None,
            body=body
        )