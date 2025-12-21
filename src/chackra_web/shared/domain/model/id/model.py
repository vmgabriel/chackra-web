from typing import Any

import pydantic


class BaseId(pydantic.BaseModel):
    value: str

    def __str__(self) -> str:
        return self.value

    def model_dump(self, *args, **kwargs) -> Any:
        return str(self.value)