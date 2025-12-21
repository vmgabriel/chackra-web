import abc

from chackra_web.shared.domain.model.web import route as shared_route
from chackra_web.shared.domain.model import extended_dependencies as shared_dependencies


class WebController(abc.ABC):
    def __init__(self, dependencies: shared_dependencies.ExtendedControllerDependencies) -> None:
        self.dependencies = dependencies

    @abc.abstractmethod
    def get_routes(self) -> list[shared_route.RouteDefinition]:
        raise NotImplementedError()