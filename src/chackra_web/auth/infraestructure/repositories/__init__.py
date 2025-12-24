from chackra_web.auth.infraestructure.repositories.psycopg import (
    creator as psycopg_repository_creator,
    finder as psycopg_repository_finder
)
from chackra_web.auth.domain.models import auth as domain_auth
from chackra_web.shared.domain.model.auth import auth_id as domain_auth_id
from chackra_web.auth.domain.models import repositories as auth_repositories
from chackra_web.shared.domain.model.repository import builder as repository_builder
from chackra_web.shared.domain.model.repository import factory as repository_factory


class AuthRepositoryFactory(repository_factory.RepositoryFactory):
    repositories = {
        "psycopg": [
            repository_builder.PreDefinitionRepository(
                repository=auth_repositories.AuthBaseRepository[domain_auth.AuthUser, domain_auth_id.AuthId],
                creator=psycopg_repository_creator.PsycopgAuthCreatorRepository,
                finder=psycopg_repository_finder.PsycopgAuthFinderRepository,
            )
        ],
    }