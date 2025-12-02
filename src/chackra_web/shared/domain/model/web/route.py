from typing import Callable, List, Optional

import dataclasses
import pydantic
import enum


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


class RouteResponse(pydantic.BaseModel):
    status_code: int
    redirection: str
    flash_message: str