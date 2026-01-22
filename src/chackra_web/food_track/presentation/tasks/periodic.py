from typing import Any

from chackra_web.shared.domain.model import extended_dependencies as shared_dependencies
from chackra_web.shared.domain.model.tasks import base as shared_model_tasks


class SendListToBuyForTeam(shared_model_tasks.Task):
    name = "send_list_to_buy_for_team"

    def execute(
        self,
        dependencies: shared_dependencies.ExtendedControllerDependencies | None = None,
        **kwargs
    ) -> Any:
        configuration = dependencies.configuration
        notification_adapter = dependencies.notification_adapter
        notification_adapter.send_message(
            recipient_id=configuration.current_channel_id,
            message="Si esto funciona ya tenemos la integracion con celery, notificaciones y celery beat"
        )


class FoodTrackTaskRegistry(shared_model_tasks.TaskRegistry):
    def __init__(self) -> None:
        super().__init__(namespace="food_track")


food_track_registry = FoodTrackTaskRegistry()
food_track_registry.register(SendListToBuyForTeam)

send_list_to_buy_for_team = shared_model_tasks.PeriodicTask(
    name="send_list_to_buy_for_team",
    namespace="food_track",
    task=SendListToBuyForTeam(),
    schedule={"cron": "*/2 * * * *"},
    kwargs={},
)