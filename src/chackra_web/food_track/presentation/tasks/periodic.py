from typing import Any

from chackra_web.shared.domain.model import extended_dependencies as shared_dependencies
from chackra_web.shared.domain.model.tasks import base as shared_model_tasks

from chackra_web.food_track.application.to_buy import (
    generate_with_llm as application_generate_with_llm,
    recommendation_with_llm as application_recommendation_with_llm
)

from chackra_web.shared.domain.model.user import user_id as shared_user_id


class SendListToBuyForTeam(shared_model_tasks.Task):
    name = "send_list_to_buy_for_team"

    def execute(
        self,
        dependencies: shared_dependencies.ExtendedControllerDependencies | None = None,
        **kwargs
    ) -> Any:
        log = dependencies.logger
        if not dependencies.configuration.all_services_user_ids or dependencies.configuration.all_services_user_ids == "":
            log.info("There are not user id")
            return

        for user_id in dependencies.configuration.all_services_user_ids:
            log.info(f"Sending list to buy for user {user_id}")
            if user_id == "":
                return
            application_generate_with_llm.GenerateWithLLMCommand(dependencies=dependencies).execute(
                shared_user_id.UserId(value=user_id)
            )


class SendRecommendationsMenu(shared_model_tasks.Task):
    name = "send_recommendations_menu"

    def execute(self, dependencies: shared_dependencies.ExtendedControllerDependencies | None = None, **kwargs) -> Any:
        log = dependencies.logger
        if not dependencies.configuration.all_services_user_ids or dependencies.configuration.all_services_user_ids == "":
            log.info("There are not user id")
            return

        for user_id in dependencies.configuration.all_services_user_ids:
            log.info(f"Sending recommendations to buy for user {user_id}")
            if user_id == "":
                return

            application_recommendation_with_llm.RecommendationMenuLLMCommand(dependencies=dependencies).execute(
                shared_user_id.UserId(value=user_id)
            )


class FoodTrackTaskRegistry(shared_model_tasks.TaskRegistry):
    def __init__(self) -> None:
        super().__init__(namespace="food_track")


food_track_registry = FoodTrackTaskRegistry()
food_track_registry.register(SendListToBuyForTeam)
food_track_registry.register(SendRecommendationsMenu)


send_list_to_buy_for_team = shared_model_tasks.PeriodicTask(
    name="send_list_to_buy_for_team",
    namespace="food_track",
    task=SendListToBuyForTeam(),
    # schedule={"cron": "*/5 * * * *"}, # For use Test
    schedule={"cron": "0 18 * * *"},
    kwargs={},
)
send_recommendations_menu = shared_model_tasks.PeriodicTask(
    name="send_recommendations_menu",
    namespace="food_track",
    task=SendRecommendationsMenu(),
    # schedule={"cron": "*/5 * * * *"}, # For use Test
    schedule={"cron": "0 8 * * *"},
    kwargs={},
)
