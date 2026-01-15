from chackra_web.shared.domain.model import extended_dependencies as shared_extended_dependencies
from chackra_web.shared.domain.model.configuration import configuration as shared_configuration
from chackra_web.shared.domain.model.tasks import base as shared_task_model

from chackra_web.shared.infraestructure.tasks.celery import port as celery_port


def get_task_port(
        configuration: shared_configuration,
        dependencies: shared_extended_dependencies
) -> shared_task_model.TaskQueueAdapterApp:
    if configuration.task_adapter == "celery":
        return celery_port.CeleryPortApp(dependencies=dependencies)

    raise NotImplementedError()