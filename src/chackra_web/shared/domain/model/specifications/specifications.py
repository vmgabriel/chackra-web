from typing import Type
import abc


class Specification(abc.ABC):

    def __and__(self, other: "Specification") -> "Specification":
        return AndSpecification(self, other)

    def __or__(self, other: "Specification") -> "Specification":
        return OrSpecification(self, other)

    @abc.abstractmethod
    def to_sql(self) -> tuple[str, tuple[str, ...]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def is_satisfied_by(self, item: object) -> bool:
        raise NotImplementedError()


class AndSpecification(Specification, abc.ABC):
    specification_1: Specification
    specification_2: Specification

    def __init__(self, specification_1: Specification, specification_2: Specification) -> None:
        self.specification_1 = specification_1
        self.specification_2 = specification_2

    def is_satisfied_by(self, item: object) -> bool:
        return self.specification_1.is_satisfied_by(item) and self.specification_2.is_satisfied_by(item)


class OrSpecification(Specification):
    specification_1: Specification
    specification_2: Specification

    def __init__(self, specification_1: Specification, specification_2: Specification) -> None:
        self.specification_1 = specification_1
        self.specification_2 = specification_2

    def is_satisfied_by(self, item: object) -> bool:
        return self.specification_1.is_satisfied_by(item) or self.specification_2.is_satisfied_by(item)
