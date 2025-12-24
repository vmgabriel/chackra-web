import dataclasses


@dataclasses.dataclass(frozen=True)
class ExceptionMessage:
    title: str
    description: str
    code: str


class SystemException(Exception):
    def __init__(self, message: ExceptionMessage, status_code: int = 500) -> None:
        super().__init__()
        self.message = message
        self.status_code = status_code

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message.title} (Code: {self.message.code})"

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "title": self.message.title,
            "detail": self.message.description,
            "code": self.message.code,
            "status": self.status_code,
        }