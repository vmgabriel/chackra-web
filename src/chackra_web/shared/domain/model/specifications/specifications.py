from typing import Any, Callable
import abc


class AbstractSpecification(abc.ABC):
    def __init__(self, attribute: str, value: Any, sql_converter: Callable[[str, Any], tuple[str, tuple]]):
        self.attribute = attribute
        self.value = value
        self._sql_converter = sql_converter

    @abc.abstractmethod
    def to_sql(self) -> tuple[str, tuple]:
        raise NotImplementedError()

    @abc.abstractmethod
    def __and__(self, other: 'Specification') -> 'AndSpecification':
        raise NotImplementedError()

    @abc.abstractmethod
    def __or__(self, other: 'Specification') -> 'OrSpecification':
        raise NotImplementedError()


class BaseSpecification(AbstractSpecification):
    def __init__(self, attribute: str, value: Any, sql_converter: Callable[[str, Any], tuple[str, tuple]]):
        super().__init__(attribute, value, sql_converter)

    def to_sql(self) -> tuple[str, tuple]:
        return self._sql_converter(self.attribute, self.value)


class CompositeSpecification(AbstractSpecification, abc.ABC):
    def __init__(self, left: AbstractSpecification, right: AbstractSpecification):
        self.left = left
        self.right = right


class AndSpecification(CompositeSpecification, abc.ABC):
    ...


class OrSpecification(CompositeSpecification, abc.ABC):
    ...




class ConvertersSpecification(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def equal(attribute: str, value: Any) -> tuple[str, tuple]:
        raise NotImplementedError()

    @staticmethod
    @abc.abstractmethod
    def not_equal(attribute: str, value: Any) -> tuple[str, tuple]:
        raise NotImplementedError()

    @staticmethod
    @abc.abstractmethod
    def ilike(attribute: str, value: Any) -> tuple[str, tuple]:
        raise NotImplementedError()

    @staticmethod
    @abc.abstractmethod
    def like(attribute: str, value: Any) -> tuple[str, tuple]:
        raise NotImplementedError()

    @staticmethod
    @abc.abstractmethod
    def in_values(attribute: str, value: Any) -> tuple[str, tuple]:
        raise NotImplementedError()