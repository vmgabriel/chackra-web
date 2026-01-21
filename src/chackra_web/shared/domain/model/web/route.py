from typing import Callable, List, Optional, Any

import dataclasses
import pydantic
import enum

import abc

from chackra_web.shared.domain.model.user import user_id as shared_user_id


class HttpMethod(enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class StatusSession(enum.StrEnum):
    SUCCESS = "SUCCESS"
    TRANSIT = "TRANSIT"
    LOGOUT = "LOGOUT"


@dataclasses.dataclass
class RouteDefinition:
    path: str
    handler: Callable
    methods: List[HttpMethod]
    name: Optional[str] = None
    middleware: List[Callable[[object, Callable], Callable]] = None
    getters_allowed: List[str] = dataclasses.field(default_factory=list)
    template: Optional[str] = None
    description: Optional[str] = None

    def query_params_allowed(self) -> List[str]:
        return self.getters_allowed + ["order_by", "page", "page_size"]

    def is_valid_query_param(self, key: str) -> bool:
        name = key.split("__")[0]
        return name in self.query_params_allowed()

    def is_valid_query_param_filter(self, key: str) -> bool:
        name = key.split("__")[0]
        return name in self.getters_allowed

    def is_valid_order_by(self, key: str) -> bool:
        name = key.replace("-", "")
        return name in self.getters_allowed



class Session(pydantic.BaseModel):
    status: StatusSession
    auth_id: str
    user_id: str
    email: str
    role: str

    def get_user_id_default(self) -> shared_user_id.UserId:
        return shared_user_id.UserId(value=self.user_id)

class RouteResponse(pydantic.BaseModel):
    status_code: int
    redirection: str
    flash_message: str
    redirection_variables: dict[str, str] = pydantic.Field(default_factory=dict)
    session: Session | None = None


class RequestData(pydantic.BaseModel):
    headers: dict[str, Any] | None = None
    body: dict[str, Any] | None = None


class RequestDataFactory(abc.ABC):
    @abc.abstractmethod
    def create(self, request: object) -> RequestData:
        raise NotImplementedError()