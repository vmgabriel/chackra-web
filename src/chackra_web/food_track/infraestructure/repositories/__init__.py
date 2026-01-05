from chackra_web.food_track.infraestructure.repositories.psycopg import (
    creator as psycopg_repository_creator,
    finder as psycopg_repository_finder,
    lister as psycopg_repository_lister,
    updater as psycopg_repository_updater,
)
from chackra_web.food_track.domain.models import (
    inventory as domain_inventory,
    to_buy as domain_to_buy,
)
from chackra_web.shared.domain.model.food_track import (
    inventory_id as domain_inventory_id,
    to_buy as domain_to_buy_id,
)
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
                listener=psycopg_repository_lister.PsycopgInventoryItemListerRepository,
                updater=psycopg_repository_updater.PsycopgInventoryItemUpdaterRepository,
            ),
            repository_builder.PreDefinitionRepository(
                repository=food_track_repositories.ToBuyListRepository[
                    domain_to_buy.FoodTrackToBuy,
                    domain_to_buy_id.FoodTrackToBuyId,
                ],
                creator=psycopg_repository_creator.PsycopgToBuyCreatorRepository,
                finder=psycopg_repository_finder.PsycopgToBuyListFinderRepository,
                listener=psycopg_repository_lister.PsycopgToBuyListerRepository,
                updater=psycopg_repository_updater.PsycopgToBuyListUpdaterRepository,
            )
        ],
    }