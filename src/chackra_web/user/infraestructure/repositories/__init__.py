from chackra_web.user.infraestructure.repositories.psycopg import (
    creator as psycopg_repository_creator,
    finder as psycopg_repository_finder
)
from chackra_web.user.domain.models import user as domain_user
from chackra_web.shared.domain.model.user import user_id as domain_user_id
from chackra_web.user.domain.models import repositories as user_repositories
from chackra_web.shared.domain.model.repository import builder as repository_builder
from chackra_web.shared.domain.model.repository import factory as repository_factory


class UserRepositoryFactory(repository_factory.RepositoryFactory):
    repositories = {
        "psycopg": [
            repository_builder.PreDefinitionRepository(
                repository=user_repositories.UserBaseRepository[domain_user.User, domain_user_id.UserId],
                creator=psycopg_repository_creator.PsycopgUserCreatorRepository,
                finder=psycopg_repository_finder.PsycopgUserFinderRepository,
            )
        ],
    }