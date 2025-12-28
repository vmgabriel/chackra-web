from typing import Any

from chackra_web.shared.domain.model.specifications import (
    conversion as shared_specification_conversion,
    specifications as shared_specifications,
)


class FlaskRequestToSpecification(shared_specification_conversion.ToSpecifications):
    def to_specification(self, key: Any, value: Any) -> shared_specifications.BaseSpecification | None:
        if not isinstance(key, str):
            raise ValueError("Key must be a string")

        attribute = key
        filter = "eq"
        if key.find("__"):
            filter_separated = key.split("__")
            attribute = filter_separated[0]
            if len(filter_separated) > 1:
                filter = filter_separated[1]

        try:
            return self.specification_builder.build(attribute, filter, value)
        except ValueError:
            self.logger.warning(f"Invalid filter {filter} for attribute {attribute}")
            return None