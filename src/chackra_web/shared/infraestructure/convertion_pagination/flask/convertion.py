from chackra_web.shared.domain.model.pagination import (
    conversion as shared_pagination_conversion,
    pagination as shared_pagination
)


class FlaskRequestToPagination(shared_pagination_conversion.ToConversion):
    def to_ordered(self, key: str) -> shared_pagination.Ordered:
        current_type = shared_pagination.OrderType.ASC
        if key.startswith("-"):
            current_type = shared_pagination.OrderType.DESC
            key = key[1:]
        return self.pagination_builder.get_ordered(current_type)(key)