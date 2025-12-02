from typing import Callable, Dict, Any

import abc

from chackra_web.shared.domain.model.web import route as shared_route, controller as shared_controller
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration


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
    def __init__(self, app: object) -> None:
        self.app = app

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
