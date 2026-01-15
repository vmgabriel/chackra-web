from chackra_web.shared.domain.model.tasks import base as shared_task_base

from celery import Celery


class CeleryPortApp(shared_task_base.TaskQueueAdapterApp):
    app: Celery

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = Celery("main", broker=self.dependencies.configuration.broker_url())

    def _setup(self) -> None:
        @self.app.task
        def run_task(full_task_name: str, kwargs: dict):
            namespace, task_name = full_task_name.split(".", 1)
            registry = self.registries[namespace]
            return registry.execute(task_name, dependencies=self.dependencies, **kwargs)
        self._run_task = run_task

    def enqueue(self, full_task_name: str, kwargs: dict) -> None:
        self._run_task.delay(full_task_name, kwargs)

    def get_app_instance(self) -> Celery:
        return self.app
