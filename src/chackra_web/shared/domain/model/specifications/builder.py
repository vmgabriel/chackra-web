from typing import Any, Callable, Type

from chackra_web.shared.domain.model.specifications import specifications as shared_specifications


class SpecificationBuilder:
    converters: shared_specifications.ConvertersSpecification
    base_specification: Type[shared_specifications.BaseSpecification]
    converters_by_operator: dict[str, Callable[[str, Any, str | None], tuple[str, tuple]]]

    def __init__(
            self,
            converters: shared_specifications.ConvertersSpecification,
            base_specification: Type[shared_specifications.BaseSpecification],
    ) -> None:
        self.converters = converters
        self.base_specification = base_specification
        self.converters_by_operator = {
            "eq": self.converters.equal,
            "ne": self.converters.not_equal,
            "like": self.converters.like,
            "ilike": self.converters.ilike,
            "in": self.converters.in_values,
        }

    def build(
            self,
            attribute: str,
            operator: str,
            value: Any,
            prefix: str | None = None
    ) -> shared_specifications.BaseSpecification:
        if operator not in self.converters_by_operator:
            raise ValueError(f"Operator {operator} not found")
        return self.base_specification(
            attribute=attribute,
            value=value,
            sql_converter=self.converters_by_operator[operator],
            prefix=prefix,
        )
