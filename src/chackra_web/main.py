from typing import Callable, List, Dict, Any, Optional, Union

import functools
import abc
import dataclasses
import enum
import flask


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
    def get_routes(self) -> List[RouteDefinition]:
        pass


class WebAdapter(abc.ABC):
    @abc.abstractmethod
    def register_route(self, route: RouteDefinition) -> None:
        pass

    @abc.abstractmethod
    def build(self) -> Any:
        pass


class WebApplication(abc.ABC):

    @abc.abstractmethod
    def add_controller(self, controller: WebController) -> None:
        pass

    @abc.abstractmethod
    def configure(self, config: Dict[str, Any]) -> None:
        pass


class FlaskAdapter(WebAdapter):
    def __init__(self, app_name: str = None):
        self.app = flask.Flask(
            app_name or __name__,
            static_folder="static",
            template_folder="templates"
        )
        self.routes: List[RouteDefinition] = []

    def _wrap_handler(self, route: RouteDefinition) -> Callable:
        @functools.wraps(route.handler)
        def wrapped(*args, **kwargs):
            result = route.handler(*args, **kwargs)

            if route.template:
                if isinstance(result, dict):
                    return flask.render_template(route.template, **result)
                return flask.render_template(route.template, data=result)
            return result

        return wrapped

    def register_route(self, route: RouteDefinition) -> None:
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
        self.routes.append(route)

    def build(self) -> flask.Flask:
        return self.app


class HomeController(WebController):
    def get_routes(self) -> List[RouteDefinition]:
        return [
            RouteDefinition(
                path="/",
                handler=self.index,
                methods=[HttpMethod.GET],
                name="home",
                template="home.html"
            ),
            RouteDefinition(
                path="/about",
                handler=self.about,
                methods=[HttpMethod.GET],
                name="about",
                template="about.html"
            ),
            RouteDefinition(
                path="/contact",
                handler=self.contact,
                methods=[HttpMethod.GET],
                name="contact",
                template="contact.html"
            )
        ]

    def index(self) -> Dict:
        return {
            "title": "Inicio",
            "message": "Bienvenido a la aplicación"
        }

    def about(self) -> Dict:
        return {
            "title": "Acerca de",
            "content": "Información sobre nosotros"
        }

    def contact(self) -> Dict:
        return {
            "title": "Contacto",
            "content": "Puedes contactar con nosotros"
        }


class ChackraWebApp(WebApplication):
    def __init__(self):
        self.adapter = FlaskAdapter(__name__)
        self.controllers: List[WebController] = []
        self.config: Dict[str, Any] = {}

    def add_controller(self, controller: WebController) -> None:
        self.controllers.append(controller)

        for route in controller.get_routes():
            self.adapter.register_route(route)

    def configure(self, config: Dict[str, Any]) -> None:
        self.config.update(config)

    def build(self):
        return self.adapter.build()


def create_app() -> ChackraWebApp:
    app = ChackraWebApp()

    app.configure({
        "DEBUG": True,
        "SECRET_KEY": "tu-clave-secreta"
    })

    app.add_controller(HomeController())

    return app


app = create_app().build()


if __name__ == "__main__":
    app.run(debug=True)
