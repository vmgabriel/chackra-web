from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.tasks import base as shared_tasks

from chackra_web.entrypoints import dependences_builder

from chackra_web.shared.infraestructure import tasks as shared_tasks_infraestructure

from chackra_web.food_track.presentation.tasks import periodic as periodic_tasks


def get_periodic_task(configuration: shared_configuration.Configuration) -> shared_tasks.PeriodicTaskProxyBuilder:
    return shared_tasks_infraestructure.get_periodic_tasks(configuration=configuration)


def create_schedule_worker() -> object:
    dependencies = dependences_builder.get_extended_dependences()

    periodic_task_builder = get_periodic_task(dependencies.configuration)

    periodic_task_builder.append(periodic_tasks.send_list_to_buy_for_team)
    periodic_task_builder.append(periodic_tasks.send_recommendations_menu)

    dependencies.inject_periodic_builder_into_task_queue(periodic_task_builder)

    return dependencies.get_task_queue_instance()


def main():
    celery = create_schedule_worker()
    celery.Beat().run()

if __name__ == "__main__":
    main()
