import abc

from chackra_web.shared.domain.model.web import route as shared_route


class WebController(abc.ABC):
    @abc.abstractmethod
    def get_routes(self) -> list[shared_route.RouteDefinition]:
        raise NotImplementedError()