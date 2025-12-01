from typing import Callable, List, Dict, Any, Optional

import abc
import dataclasses
import enum

from chackra_web.domain.shared import configuration as shared_configuration


class HttpMethod(enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


@dataclasses.dataclass
class RouteDefinition:
    path: str
    handler: Callable
    methods: List[HttpMethod]
    name: Optional[str] = None
    middleware: List[Callable] = None
    template: Optional[str] = None
    description: Optional[str] = None


class WebController(abc.ABC):
    @abc.abstractmethod
    def get_routes(self) -> list[RouteDefinition]:
        raise NotImplementedError()


class WebApplication(abc.ABC):
    @abc.abstractmethod
    def add_controller(self, controller: WebController) -> None:
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
    def register_route(self, route: RouteDefinition) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def build(self) -> object:
        raise NotImplementedError()

    @abc.abstractmethod
    def _wrap_handler(self, route: RouteDefinition) -> Callable:
        raise NotImplementedError()


class WebAppFactory(WebApplication):
    def __init__(
            self,
            app_adapter: Adapter,
            configuration: shared_configuration.Configuration,
    ) -> None:
        self.adapter = app_adapter
        self.configuration = configuration
        self.controllers: list[WebController] = []
        self.config: Dict[str, Any] = {}

    def add_controller(self, controller: WebController) -> None:
        self.controllers.append(controller)

        for route in controller.get_routes():
            self.adapter.register_route(route)

    def configure(self, config: dict[str, Any]) -> None:
        self.config.update(config)

    def build(self) -> object:
        return self.adapter.build()
