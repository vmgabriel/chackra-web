import abc

from chackra_web.shared.domain.model.specifications import specifications as shared_specifications
from chackra_web.shared.domain.model.id import model as id_model


class IdEqualSpecification(shared_specifications.Specification, abc.ABC):
    ATTRIBUTE = "id"

    id_value: id_model.BaseId

    def __init__(self, id_value: id_model.BaseId) -> None:
        self.id_value = id_value

    def is_satisfied_by(self, entity) -> bool:
        return entity.id.value == self.id_value.value


class ActiveEqualSpecification(shared_specifications.Specification, abc.ABC):
    ATTRIBUTE = "active"

    active_status: bool

    def __init__(self, active_status: bool) -> None:
        self.active_status = active_status

    def is_satisfied_by(self, entity) -> bool:
        return entity.active == self.active_status


class IsActivatedSpecification(ActiveEqualSpecification, abc.ABC):
    ACTIVE_STATUS = True

    def __init__(self) -> None:
        super().__init__(self.ACTIVE_STATUS)