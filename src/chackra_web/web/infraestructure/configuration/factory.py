from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.web.infraestructure.configuration import dev as infraestructure_dev, prod as infraestructure_prod

CONFIGURATION_FACTORIES: dict[str, type[shared_configuration.Configuration]] = {
    "DEV": infraestructure_dev.ConfigurationDev,
    "PROD": infraestructure_prod.ConfigurationProd,
}


class ConfigurationFactory:
    _default_env: str = "DEV"
    env: str = "DEV"

    def __init__(self, env: str):
        self.env = env.upper()

    def build(self) -> shared_configuration.Configuration:
        try:
            return CONFIGURATION_FACTORIES[self.env]()
        except ValueError as exc:
            return CONFIGURATION_FACTORIES[self._default_env]()

