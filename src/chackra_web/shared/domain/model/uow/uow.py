from typing import Generator, Tuple, Type
import abc
import contextlib

from chackra_web.shared.domain.model.configuration import configuration as settings
from chackra_web.shared.domain.model.logger import logger as shared_logger


class Session(abc.ABC):
    logger: shared_logger.LogAdapter
    configuration: settings.Configuration

    _session: object
    _connection: object

    def __init__(
        self,
        configuration: settings.Configuration,
        logger: shared_logger.LogAdapter,
        _session: object,
        _connection: object,
    ) -> None:
        self.configuration = configuration
        self.logger = logger
        self._session = _session
        self._connection = _connection

    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def flush(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def atomic_execute(
        self, query: str, params: Tuple[str, ...] | None = None
    ) -> object:
        raise NotImplementedError()


class UOW(abc.ABC):
    logger: shared_logger.LogAdapter
    configuration: settings.Configuration
    session_factory: Type[Session]

    def __init__(
        self,
        logger: shared_logger.LogAdapter,
        configuration: settings.Configuration,
        session_factory: Type[Session],
    ):
        self.configuration = configuration
        self.logger = logger
        self.session_factory = session_factory

    @contextlib.contextmanager
    def session(self) -> Generator[Session, Session, None]:
        _conn, _session = self._open()
        self.logger.info("Opening")

        try:
            session = self.session_factory(
                configuration=self.configuration,
                logger=self.logger,
                _session=_session,
                _connection=_conn,
            )
            yield session
        finally:
            self._close(session=_session)

    @abc.abstractmethod
    def _open(self) -> Tuple[object, object]:
        raise NotImplementedError()

    @abc.abstractmethod
    def _close(self, session: object | None) -> None:
        raise NotImplementedError()
