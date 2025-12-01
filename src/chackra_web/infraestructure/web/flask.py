import flask

from chackra_web.domain.shared import configuration as shared_configuration
from chackra_web.domain.web import app as web_app


class FlaskAdapter(web_app.Adapter):
    configuration: dict[str, str] = {}

    def __init__(self) -> None:
        _flask_app = flask.Flask(__name__)

        super().__init__(_flask_app)

    def configure(self, configuration: shared_configuration.Configuration) -> None:
        self.configuration.update(configuration.dict())

    def register_route(self, route: web_app.RouteDefinition) -> None:
        getattr(self.app, "register_route", lambda _: None)(route)

    def build(self) -> object:
        return self.app


class FlaskWebApplicationFactory(web_app.WebAppFactory):
    def __init__(
            self,
            adapter: web_app.Adapter,
            configuration: shared_configuration.Configuration
    ) -> None:
        super().__init__(adapter, configuration)

