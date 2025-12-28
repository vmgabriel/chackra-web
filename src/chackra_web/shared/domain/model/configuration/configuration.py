from typing import Any, Dict


class Configuration:
    title: str = "Chackra_Web"
    debug_level: str = "INFO"

    secret_key: str = "secret"
    debug: bool = False

    host: str = "localhost"
    port: int = 8080

    uow_adapter: str = "psycopg"
    web_adapter: str = "flask"
    logger_adapter: str = "logging"
    migration_adapter: str = "psycopg"
    repository_adapter: str = "psycopg"
    specification_adapter: str = "psycopg"
    pagination_adapter: str = "psycopg"

    # Postgres
    postgres_port: int = 5432
    postgres_dbname: str = "postgres"
    postgres_host: str = "localhost"
    postgres_username: str = "ghost"
    postgres_password: str = "rider"

    def inject(self, variables: dict[str, Any]):
        for key, value in variables.items():
            setattr(self, key, value)

    def dict(self) -> Dict[str, Any]:
        return {
            "secret_key": self.secret_key,
            "debug": self.debug,
            "host": self.host,
            "port": self.port,
        }
