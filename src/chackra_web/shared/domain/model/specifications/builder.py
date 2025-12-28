from typing import Type

from chackra_web.shared.domain.model.specifications import specifications as shared_specifications


class SpecificationStore:
    specifications: dict[
        Type[shared_specifications.Specification],
        Type[shared_specifications.Specification]
    ] = {}

    def __init__(self) -> None:
        self.specifications = {}

    def add(
            self,
            specification_type: Type[shared_specifications.Specification],
            specification: Type[shared_specifications.Specification]
    ) -> None:
        if specification_type in self.specifications:
            return
        self.specifications[specification_type] = specification

    def build(
            self,
            specification_type: Type[shared_specifications.Specification]
    ) -> Type[shared_specifications.Specification]:
        if specification_type not in self.specifications:
            raise ValueError(f"Specification {specification_type} not found")
        return self.specifications[specification_type]