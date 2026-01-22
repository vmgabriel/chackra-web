from chackra_web.shared.domain.model.tasks import base as shared_task_base

from celery.schedules import crontab, schedule
from celery import Celery


class CeleryPortApp(shared_task_base.TaskQueueAdapterApp):
    app: Celery

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = Celery("main", broker=self.dependencies.configuration.broker_url())
        self._setup()

    def _setup(self) -> None:
        @self.app.task
        def run_task(full_task_name: str, kwargs: dict):
            namespace, task_name = full_task_name.split(".", 1)
            self.dependencies.logger.info(f"Namespaces - {self.registries}")
            self.dependencies.logger.info(f"Task - {namespace}.{task_name}")
            registry = self.registries[namespace]
            return registry.execute(task_name, dependencies=self.dependencies, **kwargs)
        self.run_task = run_task

    def update_configuration(self) -> None:
        if self.periodic_task_builder:
            self.periodic_task_builder.inject_name_main_function(self.run_task.name)

        self.app.conf.update(
            broker_url=self.dependencies.configuration.broker_url(),
            result_backend=self.dependencies.configuration.broker_url(),
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone=self.dependencies.configuration.timezone,
            enable_utc=True,
            beat_schedule_filename="/tmp/celerybeat-schedule",
            beat_schedule=self.periodic_task_builder.build_schedule() if self.periodic_task_builder else {},
        )

    def enqueue(self, full_task_name: str, kwargs: dict) -> None:
        self.run_task.delay(full_task_name, kwargs)

    def get_app_instance(self) -> Celery:
        return self.app


class CeleryConverterPeriodicTask(shared_task_base.ConverterPeriodicTask):
    def to_entry(self, periodic_task: shared_task_base.PeriodicTask) -> tuple:
        return (
            periodic_task.name,
            {
                "task": self.name_main_function,
                "schedule": self._normalize_schedule(periodic_task=periodic_task),
                "args": [f"{periodic_task.namespace}.{periodic_task.name}", periodic_task.kwargs],
            }
        )

    def _normalize_schedule(self, periodic_task: shared_task_base.PeriodicTask) -> schedule | crontab:
        """Convert into schedule object."""
        s = periodic_task.schedule
        if "cron" in s:
            parts = s["cron"].split()
            return crontab(
                minute=parts[0],
                hour=parts[1],
                day_of_month=parts[2],
                month_of_year=parts[3],
                day_of_week=parts[4]
            )
        elif "seconds" in s:
            return schedule(seconds=s["seconds"])
        else:
            raise ValueError("Formato de schedule no soportado")


class CeleryPeriodicTaskProxyBuilder(shared_task_base.PeriodicTaskProxyBuilder):
    def build_schedule(self) -> dict:
        schedule_dict = {}
        for ptask in self.periodic_tasks:
            name, entry = self.converter.to_entry(ptask)
            schedule_dict[name] = entry
        return schedule_dict
