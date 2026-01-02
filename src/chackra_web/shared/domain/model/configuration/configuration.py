from typing import Any, Dict
import os
from dotenv import load_dotenv

load_dotenv()


class Configuration:
    def __init__(self):
        # Web Server Configuration
        self.title = os.getenv('APP_TITLE', 'Chackra_Web')
        self.debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
        self.host = os.getenv('FLASK_HOST', '0.0.0.0')
        self.port = int(os.getenv('FLASK_PORT', '8000'))
        self.flask_env = os.getenv('FLASK_ENV', 'production')
        self.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')

        # Database Configuration
        self.postgres_host = os.getenv('POSTGRES_HOST', 'localhost')
        self.postgres_port = int(os.getenv('POSTGRES_PORT', '5432'))
        self.postgres_db = os.getenv('POSTGRES_DB', 'chackra_db')
        self.postgres_username = os.getenv('POSTGRES_USER', 'ghost')
        self.postgres_password = os.getenv('POSTGRES_PASSWORD', 'rider')
        self.postgres_dbname = os.getenv('POSTGRES_DBNAME', 'chackra_db')

        # Adapters Configuration
        self.uow_adapter = os.getenv('UOW_ADAPTER', 'psycopg')
        self.web_adapter = os.getenv('WEB_ADAPTER', 'flask')
        self.logger_adapter = os.getenv('LOGGER_ADAPTER', 'logging')
        self.migration_adapter = os.getenv('MIGRATION_ADAPTER', 'psycopg')
        self.repository_adapter = os.getenv('REPOSITORY_ADAPTER', 'psycopg')
        self.specification_adapter = os.getenv('SPECIFICATION_ADAPTER', 'psycopg')
        self.pagination_adapter = os.getenv('PAGINATION_ADAPTER', 'psycopg')
        self.to_specification_adapter = os.getenv('TO_SPECIFICATION_ADAPTER', 'flask')
        self.to_convertion_adapter = os.getenv('TO_CONVERTION_ADAPTER', 'flask')
        self.debug_level = os.getenv('DEBUG_LEVEL', 'INFO')

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
