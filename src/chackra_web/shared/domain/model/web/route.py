from typing import Callable, List, Optional, Any

import dataclasses
import pydantic
import enum

import abc


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


class RequestData(pydantic.BaseModel):
    headers: dict[str, Any] | None = None
    body: dict[str, Any] | None = None


class RequestDataFactory(abc.ABC):
    @abc.abstractmethod
    def create(self, request: object) -> RequestData:
        raise NotImplementedError()