from typing import Any, Dict


class Configuration:
    secret_key: str = "secret"
    debug: bool = False

    host: str = "localhost"
    port: int = 8080

    web_adapter: str = "flask"

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