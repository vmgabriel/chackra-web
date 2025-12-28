from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.pagination import (
    builder as shared_pagination_builder,
    conversion as shared_pagination_conversion
)

from chackra_web.shared.infraestructure.pagination.psycopg import pagination as shared_pagination_psycopg

pagination_handlers: dict[
    str,
    shared_pagination_builder.PaginationBuilder
] = {
    "psycopg": shared_pagination_builder.PaginationBuilder(
        pagination=shared_pagination_psycopg.PsycopgPagination,
        asc_ordered=shared_pagination_psycopg.PsycopgAscOrdered,
        desc_ordered=shared_pagination_psycopg.PsycopgDescOrdered,
    )
}


class PaginationFactory:
    name_configuration_attribute: str = "pagination_adapter"

    def build(self, configuration: shared_configuration.Configuration,) -> shared_pagination_builder.PaginationBuilder:
        pagination_factory_value = getattr(configuration, self.name_configuration_attribute, "psycopg").lower()
        handlers = pagination_handlers.get(pagination_factory_value)
        return handlers