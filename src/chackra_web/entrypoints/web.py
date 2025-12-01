from chackra_web.domain.shared import configuration as domain_shared_configuration
from chackra_web.domain.web import app as web_app

from chackra_web.infraestructure.configuration import factory as infraestructure_configuration_factory
from chackra_web.infraestructure.web import factory as infraestructure_web_factory


def create_app():
    factory_configuration = infraestructure_configuration_factory.ConfigurationFactory(env="DEV")
    configuration = factory_configuration.build()

    factory_web = infraestructure_web_factory.WebApplicationFactory()
    web = factory_web.build(configuration=configuration)

    return web


app = create_app()

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()

