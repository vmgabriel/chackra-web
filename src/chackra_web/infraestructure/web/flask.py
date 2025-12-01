from typing import Callable

import os
import flask
import functools

from chackra_web.domain.shared import configuration as shared_configuration
from chackra_web.domain.web import app as web_app


class FlaskAdapter(web_app.Adapter):
    configuration: dict[str, str] = {}

    def __init__(self) -> None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        template_dir = os.path.join(base_dir, 'presentation', 'templates')
        static_dir = os.path.join(base_dir, 'presentation', 'static')


        _flask_app = flask.Flask(
            __name__,
            static_url_path="",
            static_folder=static_dir,
            template_folder=template_dir,
        )

        super().__init__(_flask_app)

    def _wrap_handler(self, route: web_app.RouteDefinition) -> Callable:
        @functools.wraps(route.handler)
        def wrapped(*args, **kwargs):
            result = route.handler(*args, **kwargs)

            if route.template:
                if isinstance(result, dict):
                    return flask.render_template(route.template, **result)
                return flask.render_template(route.template, data=result)
            return result

        return wrapped

    def configure(self, configuration: shared_configuration.Configuration) -> None:
        self.configuration.update(configuration.dict())

    def register_route(self, route: web_app.RouteDefinition) -> None:
        wrapped_handler = self._wrap_handler(route)

        if route.middleware:
            for middleware in route.middleware:
                wrapped_handler = middleware(wrapped_handler)

        self.app.add_url_rule(
            route.path,
            view_func=wrapped_handler,
            methods=[method.value for method in route.methods],
            endpoint=route.name
        )

    def build(self) -> object:
        return self.app


class FlaskWebApplicationFactory(web_app.WebAppFactory):
    def __init__(
            self,
            adapter: web_app.Adapter,
            configuration: shared_configuration.Configuration
    ) -> None:
        super().__init__(adapter, configuration)

