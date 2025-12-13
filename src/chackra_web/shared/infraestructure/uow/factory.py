from typing import Type, TypeVar

from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger

from chackra_web.shared.infraestructure.uow import psycopg as shared_psycopg


T = TypeVar("T", bound=shared_uow.UOW)
U = TypeVar("U", bound=shared_uow.Session)


uow_handler_adaptee: dict[str, Type[T]] = {
    "psycopg":  shared_psycopg.PsycopgUOW,
}

uow_session_factory: dict[str, Type[U]] = {
    "psycopg":  shared_psycopg.PsycopgSession,
}



class UOWFactory:
    name_configuration_attribute: str = "uow_adapter"

    def build(self, configuration: shared_configuration.Configuration, logger: shared_logger.LogAdapter) -> T:
        uow_adaptee_value = getattr(configuration, self.name_configuration_attribute, "psycopg").lower()
        
        session_factory = uow_session_factory.get(uow_adaptee_value)
        uow_adapter = uow_handler_adaptee.get(uow_adaptee_value)

        return uow_adapter(configuration=configuration, session_factory=session_factory, logger=logger)
