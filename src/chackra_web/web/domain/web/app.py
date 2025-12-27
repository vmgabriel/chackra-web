from typing import Callable, Dict, Any

import abc

from chackra_web.shared.domain.model.web import route as shared_route, controller as shared_controller
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration

from chackra_web.auth.domain.models import auth as auth_models, repositories as auth_repositories
from chackra_web.shared.domain.model.auth import auth_id as shared_auth_id


class WebApplication(abc.ABC):
    @abc.abstractmethod
    def add_controller(self, controller: shared_controller.WebController) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def configure(self, config: Dict[str, Any]) -> None:
        raise NotImplementedError()

    def build(self) -> object:
        return self


class Adapter(abc.ABC):
    auth_repository: auth_repositories.AuthBaseRepository[auth_models.AuthUser, shared_auth_id.AuthId]
    def __init__(
            self,
            app: object,
            auth_repository: auth_repositories.AuthBaseRepository[auth_models.AuthUser, shared_auth_id.AuthId]
    ) -> None:
        self.app = app
        self.auth_repository = auth_repository

    @abc.abstractmethod
    def configure(self, config: shared_configuration.Configuration) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def register_route(self, route: shared_route.RouteDefinition) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def build(self) -> object:
        raise NotImplementedError()

    @abc.abstractmethod
    def _wrap_handler(self, route: shared_route.RouteDefinition) -> Callable:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_auth_user(self) -> shared_route.Session | None:
        raise NotImplementedError()

    @abc.abstractmethod
    def redirect_to_login(self) -> Any:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_session(self, auth_id: str) -> shared_route.Session | None:
        raise NotImplementedError()


class WebAppFactory(WebApplication):
    def __init__(
            self,
            app_adapter: Adapter,
            configuration: shared_configuration.Configuration,
    ) -> None:
        self.adapter = app_adapter
        self.configuration = configuration
        self.controllers: list[shared_controller.WebController] = []
        self.config: Dict[str, Any] = {}

    def add_controller(self, controller: shared_controller.WebController) -> None:
        self.controllers.append(controller)

        for route in controller.get_routes():
            self.adapter.register_route(route)

    def configure(self, config: dict[str, Any]) -> None:
        self.config.update(config)

    def build(self) -> object:
        return self.adapter.build()
