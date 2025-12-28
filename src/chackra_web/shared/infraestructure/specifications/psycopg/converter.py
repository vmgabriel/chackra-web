from __future__ import annotations
from typing import Any, Tuple

from chackra_web.shared.domain.model.specifications import specifications  as shared_specifications


class PsycopgConvertersSpecification(shared_specifications.ConvertersSpecification):
    @staticmethod
    def equal(attribute: str, value: Any) -> Tuple[str, tuple]:
        return f"{attribute} = %s", (value,)

    @staticmethod
    def not_equal(attribute: str, value: Any) -> Tuple[str, tuple]:
        return f"{attribute} != %s", (value,)

    @staticmethod
    def ilike(attribute: str, value: Any) -> Tuple[str, tuple]:
        return f"{attribute} LIKE %s", (f"%{value}%",)

    @staticmethod
    def like(attribute: str, value: Any) -> Tuple[str, tuple]:
        return f"{attribute} LIKE %s", (f"%{value}%",)

    @staticmethod
    def in_values(attribute: str, value: Any) -> Tuple[str, tuple]:
        value = value.split(',')
        placeholders = ','.join(['%s'] * len(value))
        return f"{attribute} IN ({placeholders})", tuple(value)

class PsycopgAndSpecification(shared_specifications.AndSpecification):
    def __and__(self, other: shared_specifications.AbstractSpecification) -> shared_specifications.AndSpecification:
        return PsycopgAndSpecification(self, other)

    def __or__(self, other: shared_specifications.AbstractSpecification) -> shared_specifications.OrSpecification:
        return PsycopgOrSpecification(self, other)

    def to_sql(self) -> Tuple[str, tuple]:
        return f"({self.left.to_sql()[0]} AND {self.right.to_sql()[0]})", self.left.to_sql()[1] + self.right.to_sql()[1]


class PsycopgOrSpecification(shared_specifications.OrSpecification):
    def __and__(self, other: shared_specifications.AbstractSpecification) -> shared_specifications.AndSpecification:
        return PsycopgAndSpecification(self, other)

    def __or__(self, other: shared_specifications.AbstractSpecification) -> shared_specifications.OrSpecification:
        return PsycopgOrSpecification(self, other)

    def to_sql(self) -> Tuple[str, tuple]:
        return f"({self.left.to_sql()[0]} OR {self.right.to_sql()[0]})", self.left.to_sql()[1] + self.right.to_sql()[1]


class PsycopgBaseSpecification(shared_specifications.BaseSpecification):
    def __and__(self, other: shared_specifications.AbstractSpecification) -> shared_specifications.AndSpecification:
        return PsycopgAndSpecification(self, other)

    def __or__(self, other: shared_specifications.AbstractSpecification) -> shared_specifications.OrSpecification:
        return PsycopgOrSpecification(self, other)

    def to_sql(self) -> Tuple[str, tuple]:
        return self._sql_converter(self.attribute, self.value)
