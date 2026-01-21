from typing import TypeVar, Generic, List, Any, Optional, Type

import abc
import enum
import pydantic

from chackra_web.shared.domain.model.configuration import configuration as shared_configuration


class MessageRole(enum.StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class BaseMessage(pydantic.BaseModel):
    role: MessageRole
    context: Optional[list[Any]] = None


T = TypeVar("T", bound=pydantic.BaseModel)
U = TypeVar("U", bound=pydantic.BaseModel)


class InputMessage(BaseMessage, Generic[T]):
    content: T


class OutputResponse(pydantic.BaseModel, Generic[U]):
    response: U | None = None
    errors: list[str] = pydantic.Field(default_factory=list)
    context: list[Any] = pydantic.Field(default_factory=list)


class GenericLLMPort(abc.ABC, Generic[T, U]):
    configuration: shared_configuration.Configuration

    """
    Puerto genérico para interactuar con un LLM.
    - T: tipo del contenido de entrada (pydantic model)
    - U: tipo de la respuesta esperada (pydantic model)
    """

    def __init__(self, configuration: shared_configuration.Configuration) -> None:
        self.configuration = configuration

    @abc.abstractmethod
    def invoke(
        self,
        messages: list[InputMessage[T]],
        response_model: Type[U],
    ) -> OutputResponse[U]:
        raise NotImplementedError()
