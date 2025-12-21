import dataclasses

from chackra_web.shared.domain.model.uow import uow as shared_uow
from chackra_web.shared.domain.model.logger import logger as shared_logger
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration


@dataclasses.dataclass
class ControllerDependencies:
    configuration: shared_configuration.Configuration
    uow: shared_uow.UOW
    logger: shared_logger.LogAdapter
