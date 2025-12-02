from typing import Type, TypeVar

from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.web.domain.web import app as web_app
from chackra_web.web.infraestructure.web import flask as flask_web

T = TypeVar("T", bound=web_app.WebAppFactory)


web_application_factories: dict[str, Type[T]] = {
    "flask":  flask_web.FlaskWebApplicationFactory,
}


web_application_adapter: dict[str, Type[web_app.Adapter]] = {
    "flask": flask_web.FlaskAdapter,
}


class WebApplicationFactory:
    name_configuration_attribute: str = "web_adapter"

    def build(self, configuration: shared_configuration.Configuration) -> T:
        web_app_factory_value = getattr(configuration, self.name_configuration_attribute, "flask").lower()

        adapter = web_application_adapter.get(web_app_factory_value)()
        print("configuration 1 - ", configuration)
        adapter.configure(configuration)

        factory = web_application_factories.get(web_app_factory_value)(adapter, configuration)
        return factory
