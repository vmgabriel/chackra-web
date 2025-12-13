from typing import List

import abc
import pydantic

from chackra_web.shared.domain.model.migration import exceptions as migration_exceptions
from chackra_web.shared.domain.model.configuration import configuration as settings
from chackra_web.shared.domain.model.logger import logger as log_model
from chackra_web.shared.domain.model.uow import uow as log_uow


class Migrator(pydantic.BaseModel):
    up: str
    rollback: str


class MigrateHandler(pydantic.BaseModel):
    name: str
    migrator: Migrator
    is_migrated: bool = False


class MigratorHandler(abc.ABC):
    migrations: List[MigrateHandler]
    logger: log_model.LogAdapter
    uow: log_uow.UOW

    configuration: settings.Configuration

    def __init__(
        self,
        configuration: settings.Configuration,
        logger: log_model.LogAdapter,
        uow: log_uow.UOW,
    ) -> None:
        self.configuration = configuration
        self.logger = logger
        self.uow = uow

        self.migrations = []

    def add_migration(self, migration: MigrateHandler) -> None:
        self.migrations.append(migration)

    def execute(self) -> None:
        with self.uow.session() as session:
            for to_migrate in self.migrations:
                self.logger.info(f"Checking Migrating {to_migrate.name}")
                if self._is_migrated(to_migrate, session):
                    self.logger.info(f"Migration {to_migrate.name} already completed")
                    continue
                try:
                    self.logger.info(f"Making Migrating {to_migrate.name}")
                    self._migrate(to_migrate, session)
                    self._mark_as_migrated(to_migrate, session)
                except migration_exceptions.MigrationFailedError as exc:
                    self.logger.error(f"Migration {to_migrate.name} failed: {exc}")
                    self.logger.warning(
                        f"Migration {to_migrate.name} failed - Making Rollback"
                    )
                    self._rollback_migration(to_migrate, session)
            session.commit()
            if all(not migration.is_migrated for migration in self.migrations):
                self.logger.info("Not Require Migrations - All Completed")

    def pre_execute(self) -> None:
        with self.uow.session() as session:
            self._check_and_execute_table_base(session)
            session.commit()

    @abc.abstractmethod
    def _check_and_execute_table_base(self, session: log_uow.Session) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def _is_migrated(
        self, to_migrate: MigrateHandler, session: log_uow.Session
    ) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def _mark_as_migrated(
        self, to_migrate: MigrateHandler, session: log_uow.Session
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def _rollback_migration(
        self, to_migrate: MigrateHandler, session: log_uow.Session
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def _migrate(self, to_migrate: MigrateHandler, session: log_uow.Session) -> None:
        raise NotImplementedError()
