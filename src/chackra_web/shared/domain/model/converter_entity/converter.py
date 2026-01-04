from typing import Any
import abc


class AbstractConverter(abc.ABC):
    @classmethod
    def render_field(cls, field_name: str, value: Any):
        method_name = f"show_{field_name}"
        method = getattr(cls, method_name, cls._default_show)
        return method(value)

    @staticmethod
    @abc.abstractmethod
    def _default_show(value: Any) -> object:
        raise NotImplementedError()
