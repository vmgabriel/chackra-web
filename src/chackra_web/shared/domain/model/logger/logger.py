import abc
import enum

from chackra_web.shared.domain.model.configuration import configuration


class DebugLevelType(enum.StrEnum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    NONE = "NONE"


class LogAdapter(abc.ABC):
    config: configuration.Configuration

    def __init__(self, config: configuration.Configuration) -> None:
        self.config = config

    def critical(self, msg: str) -> None:
        return self._message(msg=msg, status=DebugLevelType.CRITICAL)

    def info(self, msg: str) -> None:
        return self._message(msg=msg, status=DebugLevelType.INFO)

    def warning(self, msg: str) -> None:
        return self._message(msg=msg, status=DebugLevelType.WARNING)

    def error(self, msg: str) -> None:
        return self._message(msg=msg, status=DebugLevelType.ERROR)

    @abc.abstractmethod
    def _message(self, msg: str, status: DebugLevelType) -> None:
        raise NotImplementedError()
