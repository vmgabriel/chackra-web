from chackra_web.shared.domain.model.repository import builder as repository_builder
from chackra_web.shared.domain.model import dependencies as shared_dependencies


class RepositoryFactory:
    dependencies: shared_dependencies.ControllerDependencies

    name_configuration_attribute: str = "repository_adapter"
    repositories: dict[str, list[repository_builder.PreDefinitionRepository]]

    def __init__(self, dependencies: shared_dependencies.ControllerDependencies):
        self.dependencies = dependencies
        self.repositories = self.repositories or {}

    def build(self) -> repository_builder.RepositoryStore:
        repository_factory_value = getattr(self.dependencies.configuration, self.name_configuration_attribute, "psycopg").lower()
        repositories = self.repositories.get(repository_factory_value) or []
        repository_store = repository_builder.RepositoryStore(dependencies=self.dependencies)
        for repository in repositories:
            repository_store.add(repository)
        return repository_store