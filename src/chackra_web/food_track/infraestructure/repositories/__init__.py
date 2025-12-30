from chackra_web.food_track.infraestructure.repositories.psycopg import (
    creator as psycopg_repository_creator,
    finder as psycopg_repository_finder,
)
from chackra_web.food_track.domain.models import inventory as domain_inventory
from chackra_web.shared.domain.model.food_track import inventory_id as domain_inventory_id
from chackra_web.food_track.domain.models import repositories as food_track_repositories
from chackra_web.shared.domain.model.repository import builder as repository_builder
from chackra_web.shared.domain.model.repository import factory as repository_factory


class InventoryRepositoryFactory(repository_factory.RepositoryFactory):
    repositories = {
        "psycopg": [
            repository_builder.PreDefinitionRepository(
                repository=food_track_repositories.InventoryRepository[
                    domain_inventory.InventoryItem,
                    domain_inventory_id.InventoryID
                ],
                creator=psycopg_repository_creator.PsycopgInventoryCreatorRepository,
                finder=psycopg_repository_finder.PsycopgInventoryFinderRepository,
            )
        ],
    }