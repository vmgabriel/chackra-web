from chackra_web.entrypoints import dependences_builder


def create_worker() -> object:
    dependencies = dependences_builder.get_extended_dependences()

    return dependencies.get_task_queue_instance()


def main():
    celery = create_worker()
    celery.worker_main(argv=[
        "worker",
        "--loglevel=info",
    ])

if __name__ == "__main__":
    main()
