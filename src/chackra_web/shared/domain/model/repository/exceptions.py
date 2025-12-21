
class RepositoryError(Exception):
    def __init__(self, message: str):
        super().__init__(
            f"Repository error: {message}"
        )
