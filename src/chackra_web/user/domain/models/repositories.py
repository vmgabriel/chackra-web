from chackra_web.shared.domain.model import dependencies as shared_dependencies
from chackra_web.shared.domain.model.behavior import behavior as shared_behavior
from chackra_web.shared.domain.model.repository import repository as shared_repository
from chackra_web.shared.domain.model.pagination import pagination as shared_pagination

from chackra_web.user.domain.models import behavior as user_behavior

from chackra_web.shared.domain.model.user import user_id


class UserBaseRepository(shared_repository.GenericRepository[shared_behavior.M, shared_behavior.ID]):
    def __init__(
        self,
        dependencies: shared_dependencies.ControllerDependencies,
        creator: shared_behavior.CreatorBehavior[shared_behavior.M],
        finder: user_behavior.UserFinderBehavior[shared_behavior.M, shared_behavior.ID],
        listener: shared_behavior.ListerBehavior[shared_behavior.M],
        deleter: shared_behavior.DeleterBehavior[shared_behavior.ID],
    ) -> None:
        super().__init__(dependencies, creator, finder)
        self._email_finder = finder
        self._username_finder = finder
        self._unique_username_email_finder = finder
        self._listener = listener
        self._deleter = deleter

    def find_by_email(self, email: str) -> shared_behavior.M | None:
        return self._email_finder.find_by_email(email)

    def find_by_username(self, username: str) -> shared_behavior.M | None:
        return self._username_finder.find_by_username(username)

    def find_unique_by_username_and_email(self, username: str, email: str) -> shared_behavior.M | None:
        return self._unique_username_email_finder.find_unique_by_username_and_email(username, email)

    def matching(self, pagination: shared_pagination.Pagination) -> shared_pagination.Paginator:
        return self._listener.matching(pagination)

    def delete(self, id: shared_behavior.ID) -> None:
        return self._deleter.delete(id)


class AdditionalUserRepository(shared_repository.GenericRepository[shared_behavior.M, shared_behavior.ID]):
    def __init__(
        self,
        dependencies: shared_dependencies.ControllerDependencies,
        creator: shared_behavior.CreatorBehavior[shared_behavior.M],
        finder: user_behavior.AdditionalInformationUserFinderBehavior[shared_behavior.M, shared_behavior.ID],
        updater: shared_behavior.UpdaterBehavior[shared_behavior.M, shared_behavior.ID],
    ) -> None:
        super().__init__(dependencies, creator, finder)
        self._user_by_id = finder
        self._updater = updater

    def find_by_user_id(self, user_id: user_id.UserId) -> shared_behavior.M | None:
        return self._user_by_id.find_by_user_id(user_id)

    def update(self, id: shared_behavior.ID, entity: shared_behavior.M) -> shared_behavior.M:
        return  self._updater.update(id, entity)
