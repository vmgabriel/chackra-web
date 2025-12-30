from chackra_web.shared.domain.model import dependencies as shared_dependencies
from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.shared.domain.model.repository import repository as shared_repository
from chackra_web.shared.domain.model.auth import enums as auth_enums
from chackra_web.shared.domain.model.user import user_id as domain_user_id

from chackra_web.auth.domain.models import behavior as auth_behavior


class AuthBaseRepository(shared_repository.GenericRepository[shared_behavior.M, shared_behavior.ID]):
    def __init__(
        self,
        dependencies: shared_dependencies.ControllerDependencies,
        creator: shared_behavior.CreatorBehavior[shared_behavior.M],
        finder: auth_behavior.AuthFinderBehavior[shared_behavior.M, shared_behavior.ID],
        updater: auth_behavior.AuthUpdaterBehavior[shared_behavior.M, shared_behavior.ID],
        deleter: shared_behavior.DeleterBehavior[shared_behavior.ID],
    ):
        super().__init__(dependencies, creator, finder)
        self._email_finder = finder
        self._user_id_finder = finder
        self._username_finder = finder
        self._unique_username_email_finder = finder
        self._updater = updater
        self._deleter = deleter

    def find_by_email(self, email: str) -> shared_behavior.M | None:
        return self._email_finder.find_by_email(email)

    def find_by_user_id(self, user_id: domain_user_id.UserId) -> shared_behavior.M | None:
        return self._user_id_finder.find_by_user_id(user_id)

    def update(self, id: shared_behavior.ID, entity: shared_behavior.M) -> shared_behavior.M:
        return self._updater.update(id=id, entity=entity)

    def change_role(self, id: shared_behavior.ID, role: auth_enums.AuthRole) -> None:
        return self._updater.change_role(id=id, role=role)

    def delete(self, id: shared_behavior.ID) -> None:
        return self._deleter.delete(id)