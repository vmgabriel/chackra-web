import logging

from chackra_web.shared.domain.model.configuration import configuration as settings
from chackra_web.shared.domain.model.logger import logger as shared_logger


class LoggingAdapter(shared_logger.LogAdapter):
    log: logging.Logger
    level = {
        shared_logger.DebugLevelType.CRITICAL: 50,
        shared_logger.DebugLevelType.ERROR: 40,
        shared_logger.DebugLevelType.WARNING: 30,
        shared_logger.DebugLevelType.INFO: 30,
        shared_logger.DebugLevelType.NONE: 10,
    }

    def __init__(self, configuration: settings.Configuration) -> None:
        super().__init__(config=configuration)
        self.log = logging.getLogger(configuration.title)
        debug_level = shared_logger.DebugLevelType(configuration.debug_level.upper())
        self.log.setLevel(self.level[debug_level])

    def _message(self, msg: str, status: shared_logger.DebugLevelType) -> None:
        self.log.log(level=self.level[status], msg=msg)
