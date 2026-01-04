from typing import Type, TypeVar, Callable

from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.web.domain.web import app as web_app
from chackra_web.web.infraestructure.web import flask as flask_web
from chackra_web.shared.domain.model import extended_dependencies as shared_extended_dependencies

from chackra_web.auth.domain.models import auth as auth_models, repositories as auth_repositories
from chackra_web.shared.domain.model.auth import auth_id as shared_auth_id


T = TypeVar("T", bound=web_app.WebAppFactory)


web_application_factories: dict[str, Type[T]] = {
    "flask":  flask_web.FlaskWebApplicationFactory,
}


web_application_adapter: dict[str, Type[web_app.Adapter]] = {
    "flask": flask_web.FlaskAdapter,
}


class WebApplicationFactory:
    name_configuration_attribute: str = "web_adapter"

    def build(
            self,
            configuration: shared_configuration.Configuration,
            dependencies: shared_extended_dependencies.ExtendedControllerDependencies,
            processers_handlers: list[Callable] | None = None
    ) -> T:
        web_app_factory_value = getattr(configuration, self.name_configuration_attribute, "flask").lower()

        adapter = web_application_adapter.get(web_app_factory_value)(
            auth_repository=dependencies.repository_store.build(
                auth_repositories.AuthBaseRepository[auth_models.AuthUser, shared_auth_id.AuthId],
            ),
            pagination_builder=dependencies.paginator_builder,
            to_specification_builder=dependencies.to_specification_builder,
            to_pagination_builder=dependencies.to_pagination_builder,
            processers_handlers=processers_handlers,
        )
        adapter.configure(configuration)

        factory = web_application_factories.get(web_app_factory_value)(adapter, configuration)
        return factory
