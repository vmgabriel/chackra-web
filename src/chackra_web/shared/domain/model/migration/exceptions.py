class MigrationFailedError(Exception):
    message = "Migration not completed"


class MigrationsNotCompletedError(Exception):
    message = "Migrations Not completed"