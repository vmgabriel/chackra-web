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

    def find_by_attribute(self, attribute: str) -> AbstractSpecification | None:
        if self.attribute == attribute:
            return self
        return None

    def find_and_replace_by_attribute(self, attribute: str, to_replace: AbstractSpecification) -> AbstractSpecification:
        if self.attribute == attribute:
            return to_replace
        return None


class CompositeSpecification(AbstractSpecification, abc.ABC):
    def __init__(self, left: AbstractSpecification, right: AbstractSpecification):
        self.left = left
        self.right = right

    def find_and_replace_by_attribute(self, attribute: str, to_replace: AbstractSpecification) -> AbstractSpecification:
        if isinstance(self.left, (AndSpecification, OrSpecification)):
            self.left.find_and_replace_by_attribute(attribute, to_replace)
        else:
            if self.left.attribute == attribute:
                self.left = to_replace
        if isinstance(self.right, (AndSpecification, OrSpecification)):
            self.right.find_and_replace_by_attribute(attribute, to_replace)
        else:
            if self.right.attribute == attribute:
                self.right = to_replace
        return self

    def find_by_attribute(self, attribute: str) -> AbstractSpecification | None:
        if isinstance(self.left, (AndSpecification, OrSpecification)):
            if in_left := self.left.find_by_attribute(attribute):
                return in_left
        else:
            if self.left.attribute == attribute:
                return self.left
        if isinstance(self.right, (AndSpecification, OrSpecification)):
            if in_right := self.right.find_by_attribute(attribute):
                return in_right
        else:
            if self.right.attribute == attribute:
                return self.right
        return None


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