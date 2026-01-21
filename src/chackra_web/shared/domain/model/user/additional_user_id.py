from typing import Any
from chackra_web.shared.domain.model.id import model as shared_id


class AdditionalUserId(shared_id.BaseId):
    def __str__(self) -> str:
        return self.value

    def model_dump(self, *args, **kwargs) -> Any:
        return str(self.value)