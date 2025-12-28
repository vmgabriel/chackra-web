from typing import Type

from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.logger import logger as shared_logger

from chackra_web.shared.domain.model.specifications import specifications as shared_specifications, generics as shared_generics
from chackra_web.shared.infraestructure.specifications.psycopg import generics as shared_generics_psycopg


specifications_handlers: dict[
    str,
    dict[
        Type[shared_specifications.Specification],
        Type[shared_specifications.Specification]
    ]
] = {
    "psycopg":  {
        shared_specifications.AndSpecification: shared_generics_psycopg.PsycopgAndSpecification,
        shared_specifications.OrSpecification: shared_generics_psycopg.PsycopgOrSpecification,
        shared_generics.IdEqualSpecification: shared_generics_psycopg.PsycopgIdEqualSpecification,
        shared_generics.ActiveEqualSpecification: shared_generics_psycopg.PsycopgActiveEqualSpecification,
        shared_generics.IsActivatedSpecification: shared_generics_psycopg.PsycopgActiveEqualSpecification,
    },
}


class SpecificationsGenericsFactory:
    name_configuration_attribute: str = "specification_adapter"

    def build(
            self,
            configuration: shared_configuration.Configuration,
            logger: shared_logger.LogAdapter,
    ) -> dict[Type[shared_specifications.Specification], Type[shared_specifications.Specification]]:
        specification_factory_value = getattr(configuration, self.name_configuration_attribute, "psycopg").lower()
        handlers = specifications_handlers.get(specification_factory_value)
        return handlers
